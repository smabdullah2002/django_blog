from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
import requests


# local imports
from .models import UserModel
from .serializers import UserRegistrationSerializer
from _applib.email_sender import send_otp_email


class UserRegistrationView(APIView):
    
    def send_otp(self, email,user_name):
        url = "http://127.0.0.1:8000/otp/send/"
        payload={
            "user_email": email,
            "user_name": user_name,
        }
        otp_scripts= requests.post(
            url=url,
            data=payload
        )
        
    
    def post(self, request):
        user_data=request.data
        serializer=UserRegistrationSerializer(data=user_data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user_name = serializer.validated_data.get("user_name")
            if UserModel.objects.filter(email=email).exists():
                return Response(
                    {"message": "Email already exists"},
                    status=400
                )
            if UserModel.objects.filter(user_name=user_name).exists():
                return Response(
                    {"message": "Username already exists"},
                    status=400
                )

            serializer.save()
            self.send_otp(email, user_name)
            
            return Response(
                {"message": "Registration successful", "data": serializer.data},
                status=201
            )
        else:
            return Response(
                {"message": "Registration failed", "errors": serializer.errors},
                status=400
            )