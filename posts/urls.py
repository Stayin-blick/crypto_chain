from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),  
    path('<slug:slug>/', views.post_detail, name='post_detail'),  
    path('post/new/', views.post_create, name='post_create'),  
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),  
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:post_slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:post_slug>/comment/<int:comment_id>/like/', 
            views.like_comment, name='like_comment'),
    path('<slug:slug>/edit_comment/<int:comment_id>/', 
            views.comment_edit, name='edit_comment'),
    path('<slug:slug>/delete_comment/<int:comment_id>/', 
            views.comment_delete, name='comment_delete'),
]
