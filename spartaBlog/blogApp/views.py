# coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import AddCommentForm
from models import Comment


@login_required
def comments(request):
    add_form = AddCommentForm()
    if request.method == "POST":
        add_form = AddCommentForm(request.POST)
        if add_form.is_valid():
            # сохраняем коментарий в базе
            add_comment = add_form.save(commit=False)
            add_comment.user_name = request.user.username
            add_comment.email = request.user.email
            add_comment.save()

    all_comments = Comment.objects.all()
    prepare_comments = list()
    if all_comments.count():
        for comment in all_comments:
            prepare_comments.append({"user_name": comment.user_name, "email": comment.email, "message": comment.message})

    context = {"form": add_form, "comments": prepare_comments}

    return render(request, template_name='blog/comments.html', context=context)
