from django.db.models import F
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from blog.forms import CommentForm, PostForm
from blog.models import Post, Category, Tag, Comments

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


class PostDetail(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse('post_detail', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['form'] = CommentForm()
        context['comments'] = Comments.objects.filter(post=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.get_object()

        try:
            parent_id = self.request.POST.get('parent_id')
        except:
            parent_id = None

        if parent_id:
            parent = Comments.objects.get(pk=parent_id)
            comment.parent = parent
        comment.save()
        return super(PostDetail, self).form_valid(form)


class MyPosts(ListView):
    template_name, context_object_name, paginate_by, allow_empty = base_blog(allow_empty=True)

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort:
            return Post.objects.filter(author=self.request.user).order_by(f'-{sort}')
        else:
            return Post.objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_data_sort(self, context)
        context['title'] = 'Мои посты'
        return context


class AddPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super(AddPost, self).form_valid(form)


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
