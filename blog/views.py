from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post, Category, Tag


sort_list = {
    'created_date': 'По времени',
    'likes': 'По лайкам',
    'views': 'По просмотрам'
}


def base_blog():
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = False
    return template_name, context_object_name, paginate_by, allow_empty


class Blog(ListView):
    model = Post
    template_name, context_object_name, paginate_by, allow_empty = base_blog()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort')
        sort = sort if sort else 'created_date'
        context['sort'] = sort_list[sort]
        context['title'] = 'Blog'

        return context

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort:
            return Post.objects.order_by(f'-{sort}')
        else:
            return Post.objects.all()


class PostByCategory(ListView):
    template_name, context_object_name, paginate_by, allow_empty = base_blog()

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort:
            return Post.objects.filter(category__slug=self.kwargs['slug']).order_by(f'-{sort}')
        else:
            return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort')
        sort = sort if sort else 'created_date'
        context['sort'] = sort_list[sort]
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostByTag(ListView):
    template_name, context_object_name, paginate_by, allow_empty = base_blog()
    allow_empty = False

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort:
            return Post.objects.filter(tags__slug=self.kwargs['slug']).order_by(f'-{sort}')
        else:
            return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort')
        sort = sort if sort else 'created_date'
        context['sort'] = sort_list[sort]
        context['title'] = str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context
