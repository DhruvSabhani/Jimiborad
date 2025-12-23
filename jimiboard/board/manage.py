from django.contrib.auth.base_user import BaseUserManager


# Custom User Manage
class UserManage(BaseUserManager):
    use_in_migrations = True

    def create_user(self, emailID=None, phoneNumber=None, **extra_fields):
        if not emailID and not phoneNumber:
            raise ValueError("Email or phone number is required")

        if emailID:
            emailID = self.normalize_email(emailID)  # email lowercase

        user = self.model(emailID=emailID, phoneNumber=phoneNumber, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user
