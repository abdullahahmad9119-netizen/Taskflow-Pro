from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ("id", "email", "full_name", "password", "role")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('id', 'full_name', 'email', 'role', 'bio', 'avatar', 'date_joined')
        read_only_fields = ('id', 'email', 'role', 'date_joined')

class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True, min_length=8)
    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("old password is incorrect")
        return value
class LogoutSerializer(serializers.Serializer):
    refresh= serializers.CharField(required=True)