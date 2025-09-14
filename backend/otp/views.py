from django.shortcuts import render
from rest_framework.views import APIView
from requests import request
from .models import OtpModel
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

# local imports
from .otp_generator import ran_otp
from .models import OtpModel
from .serializers import OtpValidatorSerializer
from _applib.email_sender import send_otp_email
from accounts.models import UserModel


class OtpSenderView(APIView):
    def post(self,request):
        data=request.data
        
        OtpModel.objects.filter(
            user_email=data.get("user_email"),
            status="Initialize"
        ).update(status="Expired")
        
        current_time=timezone.now()
        duration= timedelta(minutes=2)
        generated_otp= ran_otp()
        
        send_otp_email(
            user_mail=data.get("user_email"),
            otp=generated_otp
        )
        
        otp_instance= OtpModel.objects.create(
            user_email=data.get("user_email"),
            user_name=data.get("user_name"),
            otp_code=make_password(str(generated_otp)),
            message=data.get("message"),
            expires_at=current_time + duration,
            status="Initialize",
        ) 
        
        
        
        return Response(
            {"message": "OTP sent successfully."},
        )
        
        
class OtpValidatorView(APIView):
    def post(self,request):
        data=request.data
        serializer= OtpValidatorSerializer(data=data)
        if serializer.is_valid():
            valid_data= serializer.validated_data
            user_email=valid_data.get("user_email")
            otp_code= valid_data.get("otp_code")
            
            otp_obj= OtpModel.objects.filter(
                user_email=user_email,
                status="Initialize"
            ).last()
            
            if not otp_obj:
                return Response(
                    {"is_valid": False, "message": "no otp found"},
                    status=400
                )
            
            user_obj=UserModel.objects.filter(
                email=user_email, 
            ).first()
            
            if not user_obj:
                return Response(
                    {"is_valid": False, "message": "no user found"},
                    status=400
                )
                
            user_otp=otp_obj.otp_code
            expire_time= otp_obj.expires_at
            current_time= timezone.now()
            
            if expire_time<current_time:
                otp_obj.status="Expired"
                otp_obj.save()
                data={
                    "is_valid": False,
                    "message": "otp expired"
                }
            elif check_password(otp_code, user_otp) and otp_obj.status not in ["Expired", "Approved"]:
                otp_obj.status="Approved"
                
                user_obj.role="Admin"
                user_obj.save()
                
                otp_obj.verified_at= current_time
                otp_obj.save()
                data={
                    "is_valid": True,
                    "message": "otp verified"
                }
            else:
                data={
                    "is_valid": False,
                    "message": "otp invalid"
                }
                
            return Response(data)
        else:
            return Response(
                {"message":"serializer error", "errors": serializer.errors},
                status=400
            )

