from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post
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