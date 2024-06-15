from django import forms

from forum.models import CommentForum


class FormForumComments(forms.ModelForm):
    class Meta:
        model = CommentForum
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Напишите комментарий', 'id': 'floatingTextareaForum',
                       'style': 'height: 100px'}),
        }
