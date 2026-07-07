from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Post, Topic
from apps.catalog.models import HeroBanner

def post_list_view(request):
    topic_slug = request.GET.get('topic')
    posts = Post.objects.filter(is_active=True).select_related('topic')
    
    if topic_slug:
        posts = posts.filter(topic__slug=topic_slug)
        
    # Get distinct topics that have active posts
    topics = Topic.objects.annotate(
        post_count=Count('posts', filter=Q(posts__is_active=True))
    ).filter(post_count__gt=0)
    
    show_filters = topics.count() >= 2
    
    banner = HeroBanner.objects.filter(placement='BLOG_LIST', is_active=True).first()
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'topics': topics if show_filters else None,
        'current_topic': topic_slug,
        'banner': banner,
    })

def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, is_active=True)
    banner = HeroBanner.objects.filter(placement='BLOG_POST', is_active=True).first()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'banner': banner,
    })
