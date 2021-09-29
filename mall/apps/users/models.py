from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(verbose_name="手机号码", max_length=11, unique=True)

    class Meta:
        db_table = "tb_users"

