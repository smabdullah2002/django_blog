from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
import requests


# local imports
from .models import UserModel
from .serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    
    def post(self, request):
        user_data=request.data
        serializer=UserRegistrationSerializer(data=user_data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            if UserModel.objects.filter(email=email).exists():
                return Response(
                    {"message": "Email already exists"},
                    status=400
                )
            serializer.save()
            return Response(
                {"message": "Registration successful", "data": serializer.data},
                status=201
            )
        else:
            return Response(
                {"message": "Registration failed", "errors": serializer.errors},
                status=400
            )