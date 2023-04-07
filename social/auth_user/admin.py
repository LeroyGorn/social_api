from django.contrib import admin

from auth_user.models import CustomUser

admin.site.register(CustomUser)
