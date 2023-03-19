from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(
                verbose_name='photo de profile',
                upload_to='avatar',
                blank=True
                )

    def __str__(self):
        return self.username
