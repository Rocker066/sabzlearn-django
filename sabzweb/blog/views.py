from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Ticket
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.db.models import Q


def index(request):
    return render(request, 'blog/index.html')


# def post_list(request):
#     posts = Post.published.all()
#     # Instantiate paginator class to decide how many pages of posts to show
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context = {
#         'posts': posts,
#     }
#
#     return render(request, 'blog/list.html', context)


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/list.html'
    paginate_by = 3
    context_object_name = 'posts'


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)

    # Show active comments on this page
    comment = post.comments.filter(active=True)
    # show comment-form on this page
    form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }

    return render(request, 'blog/detail.html', context)


# class PostDetailView(DetailView):
#     queryset = Post.published.all()
#     template_name = 'blog/detail.html'
#     context_object_name = 'post'


def ticket(request):
    # if the request is POST, instantiate the TicketForm class
    if request.method == 'POST':
        form = TicketForm(request.POST)
        # if all form fields contain valid data then get them in a dictionary called cleaned data
        if form.is_valid():
            # create database fields based on what user has entered in the form
            # ticket_obj = Ticket.objects.create()

            # get the entered form data (as a dictionary)
            cd = form.cleaned_data

            # Another way of creating db objects (dont need to use save() here)
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject'])

            # put the user input in the related object fields in the database(from cleaned data)
            # ticket_obj.message = cd['message']
            # ticket_obj.name = cd['name']
            # ticket_obj.email = cd['email']
            # ticket_obj.phone = cd['phone']
            # ticket_obj.subject = cd['subject']
            # save the data in the database fields
            # ticket_obj.save()
            # redirect to the empty ticket page after submitting the form
            return redirect('blog:index')
    else:
        # if the user hasn't completed the form show the empty form
        form = TicketForm()
    return render(request, 'forms/ticket2.html', {'form': form})


# create a view to get the entered form info and save it (limiting this function to http-POST requests using decorator)
@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment.html', context)


# Search Field
def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            ## Search with icontains
            # result1 = Post.published.filter(title__icontains=query)
            # result2 = Post.published.filter(description__icontains=query)
            # results = result1 | result2

            ## The same search result using Q-objects
            # results = Post.published.filter(Q(title__icontains=query) | Q(description__icontains=query))

            ## The same result using Postgres FTS(Full Text Search)
            # results = Post.published.filter(Q(title__search=query) | Q(description__search=query))

            # Search using postgres Search-Vector
            results = Post.published.annotate(search=SearchVector('title',
                                                                  'description', 'slug')).filter(search=query)

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)