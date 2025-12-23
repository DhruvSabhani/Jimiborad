from .models import User
from django.core.mail import send_mail
from django.conf import settings

# DRF serializer = API validation + data handling
# Like Django Form but for APIs
from rest_framework import serializers

# re matlab pattern check (email / mobile number valid chhe ke nahi)
import re
import random


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()

    def validate_login(self, value):
        value = value.strip()  # space remove

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # check email structure
        phone_pattern = r"^[0-9]{8,15}$"  # check phone number structure

        if re.match(email_pattern, value):
            self.context["login_type"] = "email"
            return value

        if re.match(phone_pattern, value):
            self.context["login_type"] = "phone"
            return value

        if any(ch in value for ch in "<>{}()'\"`;\\"):
            raise serializers.ValidationError("Invalid characters detected")

        raise serializers.ValidationError("Enter a valid Email ID or Phone number")

    def create(self, validated_data):
        login = validated_data["login"]
        login_type = self.context["login_type"]

        code = str(random.randint(100000, 999999))  # 6 digit code

        if login_type == "email":
            user, created = User.objects.get_or_create(
                emailID=login, defaults={"emailID_code": code}
            )
            if not created:
                user.emailID_code = code
                user.save()

            self.send_email(login, code)

        else:  # phone
            user, created = User.objects.get_or_create(
                phoneNumber=login, defaults={"phoneNumber_code": code}
            )

            if not created:
                user.phoneNumber_code = code
                user.save()

            # 👉 Here you can integrate SMS API (Twilio, Fast2SMS, etc.)

        return user

    # def send_email(self, to_email, code):
    #     subject = "Jimiboard Login Code"
    #     message = f"Your login verification code is: {code}"
    #     send_mail(
    #         subject,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [to_email],
    #         fail_silently=False,
    #     )
    def send_email(self, login, code):
        subject = "Jimiboard Login Code"
        message = f"Your login verification code is: {code}"
        to = [login]
        send_mail(subject, message, settings.EMAIL_HOST_USER, to, fail_silently=False)
