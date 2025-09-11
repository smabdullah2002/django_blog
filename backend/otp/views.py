from django.shortcuts import render
from rest_framework.views import APIView
from requests import request
from .models import OtpModel
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response

# local imports
from .otp_generator import ran_otp
from .models import OtpModel
from .serializers import OtpValidatorSerializer


class OtpSenderView(APIView):
    def post(self,request):
        data=request.data
        current_time=timezone.now()
        duration= timedelta(minutes=2)
        generated_otp= ran_otp()
        otp_instance= OtpModel.objects.create(
            user_id=data.get("user_id"),
            otp_code=generated_otp,
            message=data.get("message"),
            expires_at=current_time + duration,
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
            user_id=valid_data.get("user_id")
            otp_code= valid_data.get("otp_code")
            
            otp_obj= OtpModel.objects.filter(
                user_id=user_id
            ).last()
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
            elif user_otp==otp_code and otp_obj.status!="Expired":
                otp_obj.status="Approved"
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

