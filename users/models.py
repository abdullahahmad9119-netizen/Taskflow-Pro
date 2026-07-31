from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CreateUserManager
from PIL import Image

class User(AbstractUser):
    # Attributes
    username=None
    email=models.EmailField(unique=True)
    full_name=models.CharField(max_length=40)
    avatar=models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio=models.TextField(blank=True)
    role=models.CharField(choices=[("admin", "ADMIN"), ("manager", "MANAGER"), ("member", "MEMBER")], default="member")
    # take email as username
    USERNAME_FIELD = 'email'
    # ask about fullname except email and password
    REQUIRED_FIELDS =['full_name']

    objects=CreateUserManager()