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


# home page
def index(request):
    posts = Post.objects.active().order_by('-publish')
    if request.user.is_authenticated:
        posts=Post.objects.exclude(~Q(user=request.user),draft=True)
    paginator = Paginator(posts, 5)
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

#post details
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.draft:
        if post.user != request.user:
            messages.error(request,'you have not permission to see that post',extra_tags='alert alert-danger')
            return redirect('posts:index')
    form=CommentForm(request.POST or None)
    # add comment
    if form.is_valid() and request.user.is_authenticated:
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

#create new post
@login_required(login_url='accounts:login')
def create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user=request.user
        instance.read_time=get_read_time(instance.content)
        instance.save()
        messages.success(request, 'post created successfully', extra_tags='alert-success')
        return redirect('posts:detail',instance.id)
    context = {'form': form,'title':'create post'}
    return render(request, 'post_create.html', context)

#edit post
@login_required(login_url='accounts:login')
def edit(request, pk):
    post=request.user.post_set.filter(pk=pk)
    if not post:
        messages.error(request,'you have not permission to edit that post',extra_tags='alert alert-danger')
        return redirect('posts:index')
    instance=get_object_or_404(Post,id=pk)
    form = PostForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('posts:detail',instance.id)
    context = {'form': form,'title':'edit post'}
    return render(request, 'post_create.html', context)

#delete post
@login_required(login_url='accounts:login')
def delete(request, pk):
    post = request.user.post_set.filter(pk=pk)
    if not post:
        messages.error(request, 'you have not permission to delete that post', extra_tags='alert alert-danger')
        return redirect('posts:index')
    instance = get_object_or_404(Post, pk=pk)
    instance.delete()
    messages.error(request, 'post deleted successfully', extra_tags='alert alert-info')
    return redirect('posts:index')
