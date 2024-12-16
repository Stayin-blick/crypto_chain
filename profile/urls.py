from django.urls import path
from . import views

urlpatterns = [
    path("edit/", views.edit_profile, name="edit_profile"),
    path("delete/", views.delete_profile, name="delete_profile"),
    path("<str:username>/", views.profile_detail, name="profile_detail"),

    # path("profile/setup/", views.profile_setup, name="profile_setup"),
]
