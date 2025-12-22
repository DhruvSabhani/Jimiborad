from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    emailID = models.EmailField(
        null=True, max_length=20, unique=True, blank=True, verbose_name="Email ID"
    )
    emailID_code = models.CharField(
        null=True, max_length=10, blank=True, verbose_name="Email_ID Code"
    )
    countryCode = models.CharField(
        null=True, max_length=10, blank=True, verbose_name="Country Code"
    )
    phoneNumber = models.CharField(
        null=True, max_length=20, blank=True, verbose_name="Phone number"
    )
    phoneNumber_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="Phone number Code"
    )
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

    USERNAME_FIELD = "emailID"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.emailID or self.phoneNumber or str(self.id)
