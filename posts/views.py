from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from comments.forms import CommentForm
from comments.models import Comment
from .utils import get_read_time
from django.contrib.auth.decorators import login_required

def index(request):
    posts = Post.objects.active().order_by('-timestamp')
    if request.user.is_authenticated():
        posts=Post.objects.exclude(~Q(user=request.user),draft=True)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    pages = range(1, paginator.num_pages + 1)
    context = {'posts': posts, 'pages': pages}
    return render(request, 'index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form=CommentForm(request.POST or None)
    print get_read_time(post.content)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.post=post
        parent=None
        try:
            parent_id=int(request.POST.get('parent_id'))
        except:
            parent_id=None
        if parent_id:
            query=Comment.objects.filter(id=parent_id)
            if query.exists():
                parent=query.first()
        instance.parent=parent
        instance.save()
        return redirect('posts:detail',pk)
    return render(request, 'detail.html', {'post': post,'comment_form':form})

@login_required(login_url='accounts:login')
def create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        ins = form.save(commit=False)
        ins.user=request.user
        ins.save()
        messages.success(request, 'post created successfully', extra_tags='alert-success')
        return redirect('posts:index')
    context = {'form': form}
    return render(request, 'post_create.html', context)


def edit(request, pk):
    if request.user.is_authenticated():
        post=request.user.post_set.filter(pk=pk)
        if not post:
            messages.error(request,'not permission')
            return redirect('posts:index')
    else:
        messages.error(request, 'login first')
        return redirect('posts:index')
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('posts:index')
    context = {'form': form}
    return render(request, 'post_create.html', context)


def delete(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    instance.delete()
    messages.error(request, 'post deleted successfully', extra_tags='alert-error')
    return redirect('posts:index')
