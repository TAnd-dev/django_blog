from django import forms

from blog.models import Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Напишите комментарий', 'id': 'floatingTextarea2',
                       'style': 'height: 100px'}),
        }
