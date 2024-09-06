from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post_list(request):
    posts = Post.published.all()

    context = {
        'posts': posts,
    }

    return render(request, 'blog/list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)

    context = {
        'post': post,
    }

    return render(request, 'blog/detail.html', context)