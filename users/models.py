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
    role=models.CharField(choices=[(1, "ADMIN"), (2, "MANAGER"), (3, "MEMBER")], default=3)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['full_name']

    objects=CreateUserManager()