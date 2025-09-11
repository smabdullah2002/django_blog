from django.db import models
from _applib.model_choice_fields import Status

class OtpModel(models.Model):
    user_id= models.CharField(max_length=100)
    otp_code= models.CharField(max_length=10)
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.INITIALIZE)
    message=models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()
    verified_at=models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user_id + " - " + self.otp_code+ " - " + self.status
    class Meta:
        verbose_name= "OTP Model"
        verbose_name_plural= "OTP Models"
        db_table= "otp_model"
    
