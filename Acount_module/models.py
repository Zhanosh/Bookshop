from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAcount(AbstractUser):
    avatar = models.ImageField(upload_to='avatar_img', verbose_name='عکس پروفایل')
    email_activate_code = models.CharField(max_length=200, verbose_name='کد فعالسازی حساب کاربری')

    def __str__(self):
        if self.first_name and self.last_name is not None:
            return self.get_full_name()
        else:
            return self.email
