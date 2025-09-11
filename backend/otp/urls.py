from django.urls import path
from .views import OtpSenderView, OtpValidatorView

urlpatterns=[
    path('send/', OtpSenderView.as_view(), name='otp_send'),
    path('validate/', OtpValidatorView.as_view(), name='otp_validate'),
]

#http://127.0.0.1:8000/otp/send/
#http://127.0.0.1:8000/otp/validate/