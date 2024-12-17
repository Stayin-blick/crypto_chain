from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('<str:ticker>/', views.community_detail, name='community_detail'),
    # path('join/<str:ticker>/', views.join_community, name='join_community'),
]
