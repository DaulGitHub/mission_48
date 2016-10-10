# coding: utf8
from django import forms
from models import Comment, Post, PrivateMessage


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


class AddPrivateMessageForm(forms.ModelForm):
    """Форма добавлениия личного сообщения"""

    class Meta:
        model = PrivateMessage
        fields = ('message', )
