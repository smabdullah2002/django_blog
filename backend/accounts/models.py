from django.db import models
from _applib.model_choice_fields import Role
from django.utils import timezone
from datetime import timedelta

class UserModel(models.Model):
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    user_name = models.CharField(max_length=150, unique=True, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  #
    password = models.CharField(max_length=100, blank=False, null=False)
    role = models.CharField(choices=Role.choices, default=Role.VIEWER, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email + " ---- " + self.user_name
    
    class Meta:
        verbose_name = "User_table"
        verbose_name_plural = "Users_table"
        db_table = "users_table"


class FailedLoginAttempt(models.Model):
    username_or_email = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    
    def is_blocked(self):
        block_time= timezone.now() - timedelta(minutes=10)
        return self.attempts >=5 and self.last_attempt > block_time
        
    