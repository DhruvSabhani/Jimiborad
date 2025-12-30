from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manage import UserManage
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    emailID = models.EmailField(
        null=True, max_length=255, unique=True, blank=True, verbose_name="Email ID"
    )
    emailID_hash_code = models.CharField(
        null=True, max_length=255, blank=True, verbose_name="Email_ID Code"
    )  # stores hashed code
    is_used_emailcode = models.BooleanField(default=False)
    emailcode_expires_dt = models.DateTimeField(null=True)  # code expires datetime
    countryCode = models.CharField(
        null=True, max_length=10, blank=True, verbose_name="Country Code"
    )
    phoneNumber = models.CharField(
        null=True, max_length=20, blank=True, verbose_name="Phone number"
    )
    phoneNumber_hash_code = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Phone number Code"
    )  # stores hashed code
    is_used_phonenumbercode = models.BooleanField(default=False)
    phonenumbercode_expires_dt = models.DateTimeField(
        null=True
    )  # code expires datetime
    username = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Username"
    )
    userImg = models.ImageField(
        upload_to="Images/", null=True, blank=True, verbose_name="User Image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created DateTime"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated DateTime")
    last_logout_dt = models.DateTimeField(
        null=True, blank=True, verbose_name="Last_logout DateTime"
    )

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []
    objects = UserManage()

    def is_expired(self):
        now = timezone.now()
        if self.emailcode_expires_dt and now > self.emailcode_expires_dt:
            return True
        if self.phonenumbercode_expires_dt and now > self.phonenumbercode_expires_dt:
            return True
        return False

    def __str__(self):
        return self.emailID or self.phoneNumber or str(self.id)
