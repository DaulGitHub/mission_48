# coding: utf8
from django import forms
from models import Comment, Post


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class AddCommentForm(forms.ModelForm):
    """Форма добавления коментария."""

    class Meta:
        model = Comment
        fields = ('message',)


class AddPostForm(forms.ModelForm):
    """Форма добавления поста."""

    class Meta:
        model = Post
        fields = ('photo', 'message')


