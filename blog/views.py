from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post


class Blog(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


def get_category(request, slug):
    return render(request, 'blog/category.html')


def get_post(request, slug):
    return render(request, 'blog/category.html')