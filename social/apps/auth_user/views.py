from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.auth_user.serializers import UserSerializer, CustomObtainTokenSerializer, UserAnalyticsSerializer

from apps.auth_user.models import CustomUser


class UserCreateView(generics.CreateAPIView):
    permission_classes = (
        AllowAny,
    )
    serializer_class = UserSerializer


class UserLoginView(TokenObtainPairView):
    permission_classes = (
        AllowAny,
    )
    serializer_class = CustomObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = get_object_or_404(CustomUser, email=request.data.get('email'))
        user.last_session = timezone.now()
        user.save()
        return response


class UserLogoutView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
            return Response("Successful Logout", status=status.HTTP_205_RESET_CONTENT)
        except Exception as exc:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAnalyticsView(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = UserAnalyticsSerializer

    def get(self, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        return Response(
            UserAnalyticsSerializer(user).data
        )
