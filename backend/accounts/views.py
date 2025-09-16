from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
import requests
from django.utils import timezone
from datetime import timedelta

# local imports
from .models import UserModel, FailedLoginAttempt
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

class UserLoginView(APIView):
    def post(self, request):
        data= request.data
        
        username_or_email=data.get("username_or_email")
        password=data.get("password")
        ip_address=request.META.get('REMOTE_ADDR')
        
        print("IP Address:", ip_address)
        
        attempt, created= FailedLoginAttempt.objects.get_or_create(
            username_or_email=username_or_email,
            ip_address=ip_address
        )
        
        if attempt.is_blocked():
            return Response(
                {"message": "Too many failed login attempts. Please try again later."},
                status=429
            )

        if "@" in username_or_email:
            # Login with email
            user_obj = UserModel.objects.filter(email=username_or_email).first()
        else:
            # Login with username
            user_obj = UserModel.objects.filter(user_name=username_or_email).first()
        if user_obj and check_password(password, user_obj.password):
            
            # Reset failed attempts on successful login
            attempt.attempts = 0
            attempt.save()
            print("Login successful")
            return Response(
                {"message": "Login successful", "data": {"user_name": user_obj.user_name}},
                status=200
            )
        else:
            # Increment failed attempts on failed login
            attempt.attempts += 1
            attempt.last_attempt = timezone.now()
            attempt.save()
            return Response(
                {"message": "Invalid username/email or password"},
                status=401
            )
