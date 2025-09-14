from rest_framework import serializers


class OtpValidatorSerializer(serializers.Serializer):
    user_email= serializers.EmailField(max_length=100)
    otp_code= serializers.CharField(max_length=6)