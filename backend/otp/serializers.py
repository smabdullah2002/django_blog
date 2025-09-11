from rest_framework import serializers


class OtpValidatorSerializer(serializers.Serializer):
    user_id= serializers.CharField(max_length=100)
    otp_code= serializers.CharField(max_length=6)