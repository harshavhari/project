from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

@login_required
def blog_list(request):
    blogs = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    comments = blog.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments, 'form': form})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_edit(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_delete(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})
