from django.shortcuts import render, get_object_or_404
#
from django.core.paginator import Paginator
#
from .models import Post



# Create your views here.

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post/list.html', {'posts': page_obj})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post':post})