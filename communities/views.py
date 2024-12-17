from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Community
from posts.models import Post, Comment, Like

# View for displaying all communities
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'communities/community_list.html', {'communities': communities})

# View for displaying details of a single community, including posts
def community_detail(request, ticker):
    community = get_object_or_404(Community, ticker=ticker)
    posts = Post.objects.filter(community=community)  # If you have posts tied to communities
    return render(request, 'communities/community_detail.html', {'community': community, 'posts': posts})

