from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse

from .forms import PostForm
from .models import Group, Post


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'posts': post_list})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()[:12]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {
        'group': group,
        'page': page,
        'paginator': paginator
    }
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(reverse('index'))
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = profile.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    count = posts.count()
    return render(request, 'profile.html', {
        'profile': profile,
        'posts': posts,
        'page': page,
        'paginator': paginator,
        'count': count
    }
    )


def post_view(request, username, post_id):
    posts = get_object_or_404(Post, pk=post_id, author__username=username)
    return render(request, 'post.html', {
        'profile': posts.author,
        'posts': posts,
        'post_id': post_id,
    }
    )


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = User.objects.get(username=username)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    if request.user != profile:
        return redirect(reverse('post', kwargs={
            'username': username,
            'post_id': post_id
        }
        ))

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(reverse('post', kwargs={
            'username': username,
            'post_id': post_id
        }
        ))

    return render(request, 'new_post.html', {
        'form': form,
        'profile': profile,
        'edit': True,
        'post': post
    }
    )


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
