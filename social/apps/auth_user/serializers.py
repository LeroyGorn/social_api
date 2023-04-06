from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.auth_user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'check_password',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['check_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class CustomObtainTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data

    @classmethod
    def get_token(cls, user):
        token = super(CustomObtainTokenSerializer, cls).get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


class UserAnalyticsSerializer(serializers.ModelSerializer):
    last_session = serializers.SerializerMethodField()
    last_activity = serializers.SerializerMethodField()

    def get_last_session(self, obj):
        return obj.last_session.strftime('%Y-%m-%d %H:%M:%S') if obj.last_session else 'Never'

    def get_last_activity(self, obj):
        return obj.last_activity.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'last_session',
            'last_activity'
        ]
