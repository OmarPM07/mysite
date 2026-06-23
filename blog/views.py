from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db import models
from .models import Post



# Create your views here.

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post/list.html', {'posts': page_obj, 'tag': tag})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    
    # Incrementar contador de visitas
    Post.published.filter(id=post.id).update(views=models.F('views') + 1)
    post.refresh_from_db()
    
    # Posts relacionados por tags
    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id).distinct()[:4]
    
    return render(request, 'blog/post/detail.html', {'post':post, 'related_posts': related_posts})

