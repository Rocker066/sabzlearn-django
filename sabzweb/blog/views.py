from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Ticket
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
#
#     context = {
#         'post': post,
#     }
#
#     return render(request, 'blog/detail.html', context)


class PostDetailView(DetailView):
    queryset = Post.published.all()
    template_name = 'blog/detail.html'
    context_object_name = 'post'


def ticket(request):
    # if the request is POST, instantiate the TicketForm class
    if request.method == 'POST':
        form = TicketForm(request.POST)
        # if all form fields contain valid data then get them in a dictionary called cleaned data
        if form.is_valid():
            # create database fields based on what user has entered in the form
            ticket_obj = Ticket.objects.create()
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