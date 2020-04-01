from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost
# Create your views here.

class BlogList(ListView):
    model = BlogPost
    context_object_name = 'blog_post_list'
    template_name = 'blog/index.html'

    paginate_by = 2

class BlogDetail(DetailView):
    model = BlogPost
    context_object_name = 'blog_post'
    template_name = 'blog/blog_post.html'
