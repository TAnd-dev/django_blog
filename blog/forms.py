from django import forms

from blog.models import Comments, Post

from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Напишите комментарий', 'id': 'floatingTextarea2',
                       'style': 'height: 100px'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'photo', 'category', 'tags')

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'height: 50px', 'id': 'title'}),
            'text': SummernoteWidget(),
            'photo': forms.FileInput(
                attrs={'class': 'form-control', 'id': 'photo'}),
            'category': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-label'}
            )
        }
