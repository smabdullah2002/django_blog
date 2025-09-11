from django.db import models
from _applib.model_choice_fields import Role

class UserModel(models.Model):
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    user_name = models.CharField(max_length=150, unique=False, blank=False, null=False)
    profile_picture = models.CharField(max_length=300)
    password = models.CharField(max_length=100, blank=False, null=False)
    role = models.CharField(choices=Role.choices, default=Role.VIEWER, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "User_table"
        verbose_name_plural = "Users_table"
        db_table = "users_table"
    