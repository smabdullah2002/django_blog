from django.db import models

class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    VIEWER = "VIEWER", "Viewer"
    STUDENT = "STUDENT", "Student"
    
class Status(models.TextChoices):
    INITIALIZE= "Initialize",
    APPROVED= "Approved",
    EXPIRED= "Expired",