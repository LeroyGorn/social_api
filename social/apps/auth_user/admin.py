from django.contrib import admin

from apps.auth_user.models import CustomUser

admin.site.register(CustomUser)
