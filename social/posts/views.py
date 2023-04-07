from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from posts.models import UserPost, Like
from posts.serializers import LikeSerializer, UserPostSerializer, UserPostListSerializer
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PostListView(generics.ListAPIView):
    permission_classes = (
        AllowAny,
    )
    pagination_class = LimitOffsetPagination
    serializer_class = UserPostListSerializer

    def get_queryset(self):
        return UserPost.objects.all()


class PostDetailsView(generics.RetrieveAPIView):
    permission_classes = (
        AllowAny,
    )
    serializer_class = UserPostSerializer

    def get_object(self):
        return get_object_or_404(UserPost, id=self.kwargs.get('post_id'))


class UserPostView(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    pagination_class = LimitOffsetPagination
    serializer_class = UserPostSerializer

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user)


class LikeAnalyticsView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get_filter_condition(self):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        date_from = make_aware(datetime.strptime(date_from, '%Y-%m-%d')) if date_from else None
        date_to = make_aware(datetime.strptime(date_to, '%Y-%m-%d')) if date_to else None

        condition_dict = {
            'date_from': Q(created_on__gte=date_from),
            'date_to': Q(created_on__lte=date_to)
        }
        filter_condition = Q()
        for param in self.request.query_params.keys():
            filter_condition &= condition_dict.get(param, Q())
        return filter_condition

    def get(self, request):
        likes = Like.objects.filter(self.get_filter_condition())
        likes_by_day = likes.annotate(day=TruncDay('created_on')).values('day').annotate(count=Count('id'))
        return Response(likes_by_day)


class LikeView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get_user_post(self):
        return get_object_or_404(UserPost, id=self.kwargs.get('post_id'))

    def post(self, request, *args, **kwargs):
        user_post = self.get_user_post()
        if Like.objects.filter(user=request.user, post=user_post).exists():
            raise ValidationError('You have already liked this post.')

        like = Like.objects.create(post=user_post, user=request.user)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_post = self.get_user_post()
        like = get_object_or_404(Like, user=request.user, post=user_post)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
