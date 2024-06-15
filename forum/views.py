from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from forum.forms import FormForumComments
from forum.models import ThemeForum, CommentForum


class Forum(ListView):
    model = ThemeForum
    template_name = 'forum/forum.html'
    context_object_name = 'themes'
    paginate_by = 15


class ThemeDetail(FormMixin, DetailView):
    model = ThemeForum
    template_name = 'forum/theme_detail.html'
    context_object_name = 'theme'

    form_class = FormForumComments

    def get_success_url(self, **kwargs):
        return reverse('theme_detail', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['comments'] = CommentForum.objects.filter(theme=self.get_object())
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
        comment.theme = self.get_object()
        comment.save()
        return super().form_valid(form)
