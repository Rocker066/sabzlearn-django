from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post_list(request):
    return HttpResponse("Hello, world. You're at the post_list.")


def post_detail(request, pk):
    return HttpResponse(f"Hello, world. You're at the post_detail view, Post:{pk}", pk)