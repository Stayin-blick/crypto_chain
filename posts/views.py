from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Post, Comment, Like
from .forms import CommentForm


class PostList(generic.ListView):
    """
    Returns all published posts in :model:`blog.Post`
    and displays them in a page of six posts.

    **Context**

    - `queryset`: All published instances of :model:`blog.Post`
    - `paginate_by`: Number of posts per page.

    **Template:**

    :template:`blog/index.html`
    """
    queryset = Post.objects.all().order_by('-created_on')
    template_name = "posts/index.html"
    paginate_by = 6


def post_detail(request, slug):
    # Get the post object
    post = get_object_or_404(Post, slug=slug)
    
    # Check if the user has liked the post
    user_liked_post = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    
    # Check if the user has liked each comment
    user_likes_on_comments = {
        comment.id: comment.likes.filter(user=request.user).exists() for comment in post.comments.all()
    }

    # Get the comments related to the post
    comments = post.comments.all()
    
    # Create a comment form instance
    comment_form = CommentForm(request.POST or None)
    
    # Context to pass to the template
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked_post': user_liked_post,
        'user_likes_on_comments': user_likes_on_comments,
    }

    return render(request, 'posts/post_detail.html', context)

def comment_edit(request, slug, comment_id):
    """
    Allow users to edit their own comment on a post.

    **Context**

    - `post`: The related post instance.
    - `comment`: The comment being edited.
    - `comment_form`: The form for editing the comment.
    """
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        # Ensure only the comment's author can edit it
        messages.error(request, "You are not authorized to edit this comment.")
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, "Comment updated successfully!")
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        else:
            messages.error(request, "Error updating comment. Please try again.")

    else:
        # Prepopulate the form with the existing comment
        comment_form = CommentForm(instance=comment)

    return render(request, "edit_comment.html", {
        "post": post,
        "comment": comment,
        "comment_form": comment_form,
    })


def comment_delete(request, slug, comment_id):
    """
    Delete an individual comment.

    **Context**

    - `post`: An instance of the related Post.
    - `comment`: The comment to be deleted.
    """
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    # Ensure only the author or a superuser can delete the comment
    if comment.author == request.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    else:
        messages.error(request, "You are not authorized to delete this comment.")

    # Redirect to post detail after deletion
    return HttpResponseRedirect(reverse("post_detail", args=[slug]))


def post_create(request):
    """
    Allow users to create a new post.

    **Context**

    - `form`: A form for creating a new post.
    """
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return HttpResponseRedirect(reverse("post_detail", args=[post.slug]))
    else:
        form = PostForm()

    return render(request, "blog/post_create.html", {"form": form})


def post_edit(request, slug):
    """
    Allow the post's author to edit their post.

    **Context**

    - `post`: The post to be edited.
    - `form`: A form for editing the post.
    """
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, "You are not authorized to edit this post.")
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))

    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_edit.html", {"form": form, "post": post})


def post_delete(request, slug):
    """
    Allow the post's author to delete their post.

    **Context**

    - `post`: The post to be deleted.
    """
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, "You are not authorized to delete this post.")
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))

    post.delete()
    messages.success(request, "Post deleted successfully!")
    return HttpResponseRedirect(reverse("home"))


def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    # Check if the user has already liked the post
    existing_like = Like.objects.filter(post=post, user=request.user).first()

    if existing_like:
        # If the user has already liked the post, remove the like
        existing_like.delete()
        liked = 0
    else:
        # Otherwise, create a new like
        Like.objects.create(post=post, user=request.user)
        liked = 1

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })


def like_comment(request, post_slug, comment_id):
    # Get the post and comment based on the slug and comment_id
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user has already liked the comment
    existing_like = Like.objects.filter(comment=comment, user=request.user).first()

    if existing_like:
        # If the user has already liked the comment, remove the like
        existing_like.delete()
        liked = 0
    else:
        # Otherwise, create a new like
        Like.objects.create(comment=comment, user=request.user)
        liked = 1

    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes.count()  # Returns the total likes count for the comment
    })