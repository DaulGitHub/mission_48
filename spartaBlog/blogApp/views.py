# coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import AddCommentForm, AddPostForm
from models import Comment, Post
from django.core.paginator import Paginator
from django.contrib.auth.models import User


@login_required
def comments(request):
    """Страница с общими коментариями"""
    add_form = AddCommentForm()
    if request.method == "POST":
        add_form = AddCommentForm(request.POST)
        if add_form.is_valid():
            # сохраняем коментарий в базе
            add_comment = add_form.save(commit=False)
            add_comment.user_name = request.user.username
            add_comment.email = request.user.email
            add_comment.save()

    # извлекаем все коментарии
    all_comments = Comment.objects.all()
    prepare_comments = list()
    if all_comments.count():
        for comment in all_comments:
            prepare_comments.append({"user_name": comment.user_name, "message": comment.message})

    # делаем пагинацию коментариев по 3 на странице
    current_page_number = 1
    if request.GET.get("page"):
        current_page_number = int(request.GET.get("page"))
    comments_on_page = Paginator(prepare_comments, 3)
    current_page_comments = comments_on_page.page(current_page_number)

    context = {"form": add_form, "comments": current_page_comments,
               "next_page": current_page_comments.next_page_number() if current_page_comments.has_next() else current_page_number,
               "previous_page": current_page_comments.previous_page_number() if current_page_comments.has_previous() else current_page_number}

    return render(request, template_name='blog/comments.html', context=context)


@login_required
def wall(request, wall_owner=None):
    """Страница стены юзера. Пользователь может постить себе на стену и другим пользователям"""
    # определяем владельца стены
    if wall_owner == "":
        wall_owner = request.user.username

    form = AddPostForm()
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.commentator_name = request.user.username
            post.wall_owner = wall_owner
            post.save()

    # извлекаем посты хозяина стены
    posts = Post.objects.filter(wall_owner=wall_owner)
    prepared_posts = []
    for post in posts:
        prepared_posts.append({"photo": post.photo, "comment": post.message})

    # извлекаем имена всех зарегистрированных пользователей
    users = list(User.objects.values_list('username', flat=True))
    users.remove("admin")
    context = {"wall_owner": wall_owner, "all_users": users, "form": form, "posts": prepared_posts}

    return render(request, template_name='blog/wall.html', context=context)
