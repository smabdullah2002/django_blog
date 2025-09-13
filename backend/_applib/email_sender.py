from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user_mail, otp):
    subject="OTP for verifications"
    message= f"Your one time password(OTP) is : {otp}. It is valid for 2 minutes."
    from_email=settings.DEFAULT_FROM_EMAIL
    recipient_list=[user_mail]
    send_mail(subject, message, from_email, recipient_list)
    









