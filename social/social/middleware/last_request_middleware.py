import json
from django.utils import timezone

from apps.auth_user.models import CustomUser


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save()

        return response
