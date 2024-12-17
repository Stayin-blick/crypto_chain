from django.db import models
from django.contrib.auth.models import User

class Community(models.Model):
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10, unique=True)
    bio = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="community_members", blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.ticker})"

