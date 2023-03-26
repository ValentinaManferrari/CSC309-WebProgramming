from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def avatar_path(instance, filename):
    return  filename
class OurUser(AbstractUser):
    # First name, last name, email, password all included in base model
    # We only need to add extra fields
    password = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True)
    phone = models.CharField(blank=True, max_length=12)
    pass
