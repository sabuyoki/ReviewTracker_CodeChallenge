from __future__ import unicode_literals
from django.db import models
import re

class Review(models.Model):
    users = models.ForeignKey('login.User', related_name='reviewer')
    site = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    auther = models.CharField(max_length=255)
    review_date = models.CharField(max_length=255)
    likes = models.CharField(max_length=5)
    dislikes = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"News Object: ID:({ self.id }) list_name:{ self.list_name } site:{ self.site } Created At:{ self.created_at } Updated At:{ self.updated_at }"


