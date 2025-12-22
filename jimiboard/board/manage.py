from django.contrib.auth.models import BaseUserManager


# Custom User Manager
class UserManage(BaseUserManager):
    use_in_migrations = True

    def create_user(self, emailID=None, phoneNumber=None, **extra_fields):
        if not emailID and not phoneNumber:
            return ValueError("Email or phone number is required")
        if emailID:
            # upper to lower convert
            emailID = self.normalize_email(emailID)

        user = self.model(emailID=emailID, phoneNumber=phoneNumber, **extra_fields)

        user.set_unusable_password()  # no password login
        user.save(using=self._db)
        return user
