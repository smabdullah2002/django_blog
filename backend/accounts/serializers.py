from django.contrib.auth.hashers import make_password
from accounts.models import UserModel
from rest_framework import serializers
from _applib.model_choice_fields import Role 

class UserRegistrationSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=100)
    user_name=serializers.CharField(max_length=150)
    full_name= serializers.CharField(max_length=100)
    profile_picture=serializers.CharField(max_length=300)
    password=serializers.CharField(max_length=100)
    role=serializers.ChoiceField(choices=Role.choices, default=Role.VIEWER, error_messages={
        'invalid': 'Invalid role'
    })
    def create(self, validated_data):
        validated_data["password"]= make_password(validated_data["password"])
        return UserModel.objects.create(**validated_data)
    
    