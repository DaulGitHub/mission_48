# coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import AddCommentForm
from models import Comment
from django.core.paginator import Paginator


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

    current_page_number = 1
    if request.GET.get("page"):
        current_page_number = int(request.GET.get("page"))
    comments_on_page = Paginator(prepare_comments, 3)
    current_page_comments = comments_on_page.page(current_page_number)

    context = {"form": add_form, "comments": current_page_comments,
               "next_page": current_page_comments.next_page_number() if current_page_comments.has_next() else current_page_number,
               "previous_page": current_page_comments.previous_page_number() if current_page_comments.has_previous() else current_page_number}

    return render(request, template_name='blog/comments.html', context=context)
