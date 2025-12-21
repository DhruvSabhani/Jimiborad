from django.contrib.auth.models import BaseUserManager


class UserManage(BaseUserManager):
    def create_user(
        self, emailID=None, phone_number=None, password=None, **extra_fields
    ):
        if not emailID and not phone_number:
            raise ValueError("User must have an email or phone number")

        if emailID:
            emailID = self.normalize_email(emailID)

        user = self.model(emailID=emailID, phone_number=phone_number, **extra_fields)
        user.set_unusable_password()  # No password login
        user.save(using=self._db)
        return user

    def create_superuser(self, emailID, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(emailID=emailID, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
