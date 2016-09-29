# coding: utf8
from django import forms
from models import Comment

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class AddCommentForm(forms.ModelForm):
    """Форма добавления коментария."""

    class Meta:
        model = Comment
        fields = ('message',)