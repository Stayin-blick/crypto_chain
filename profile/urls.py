from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/", views.profile_detail, name="profile_detail"),
    # path("profile/setup/", views.profile_setup, name="profile_setup"),
]
