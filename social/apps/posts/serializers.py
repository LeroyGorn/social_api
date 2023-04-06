from rest_framework import serializers

from apps.posts.models import UserPost, Like


class UserPostListSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_updated_on(self, obj):
        return obj.updated_on.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserPost
        fields = ['id', 'title', 'updated_on', 'likes']


class UserPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()

    def get_updated_on(self, obj):
        return obj.updated_on.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_on(self, obj):
        return obj.created_on.strftime('%Y-%m-%d %H:%M:%S')

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = UserPost
        fields = ['id', 'title', 'content', 'created_on', 'updated_on', 'likes']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserPost.objects.create(
            author=user,
            title=validated_data['title'],
            content=validated_data['content']
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post', 'created_on']
        read_only_fields = ['user', 'created_on']

    def validate_post(self, value):
        if not value:
            raise serializers.ValidationError('Post does not exist!')
        return value

    def create(self, validated_data):
        like, created = Like.objects.get_or_create(
            post=validated_data['post'],
            user=self.context['request'].user
        )
        return like
