from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post, Category, Tag

sort_list = {
    'created_date': 'По времени',
    'likes': 'По лайкам',
    'views': 'По просмотрам'
}


def base_blog(template_name='blog/blog.html', context_object_name='posts', paginate_by=10, allow_empty=False):
    return template_name, context_object_name, paginate_by, allow_empty


def get_context_data_sort(self, context):
    sort = self.request.GET.get('sort')
    sort = sort if sort else 'created_date'
    context['sort'] = sort_list[sort]
    return context


class Blog(ListView):
    model = Post
    template_name, context_object_name, paginate_by, allow_empty = base_blog()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_data_sort(self, context)
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
        context = get_context_data_sort(self, context)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostByTag(ListView):
    template_name, context_object_name, paginate_by, allow_empty = base_blog()

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort:
            return Post.objects.filter(tags__slug=self.kwargs['slug']).order_by(f'-{sort}')
        else:
            return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_data_sort(self, context)
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


class Search(ListView):
    template_name, context_object_name, paginate_by, allow_empty = base_blog(allow_empty=True)

    def get_queryset(self):
        search = self.request.GET.get('search')
        return Post.objects.filter(title__icontains=search)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_data_sort(self, context)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context