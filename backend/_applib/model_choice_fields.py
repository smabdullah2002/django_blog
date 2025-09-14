from django.db import models

class Role(models.TextChoices):
    ADMIN = "Admin",
    VIEWER = "Viewer"

class Status(models.TextChoices):
    INITIALIZE= "Initialize",
    APPROVED= "Approved",
    EXPIRED= "Expired",