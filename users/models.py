from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='default_profile_picture.jpg'
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username