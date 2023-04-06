from django.contrib import admin

from apps.posts.models import UserPost, Like

admin.site.register(UserPost)
admin.site.register(Like)
