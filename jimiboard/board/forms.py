from .models import User
from django.core.mail import send_mail
from django.conf import settings

# Django password hashing
from django.contrib.auth.hashers import make_password

# Django timezone for expiry time
from django.utils import timezone
from datetime import timedelta

# Utility function to generate secure code
from .utils import generate_ai_secure_code

# DRF serializer = API validation + data handling
# Like Django Form but for APIs
from rest_framework import serializers

# re matlab pattern check (email / mobile number valid chhe ke nahi)
import re

# email format
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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

        code = str(generate_ai_secure_code())

        expiry = timezone.now() + timedelta(seconds=59)

        if login_type == "email":
            user, created = User.objects.get_or_create(
                emailID=login,
                defaults={
                    "emailID_hash_code": make_password(code),
                    "emailcode_expires_dt": expiry,
                },
            )
            if not created:
                user.emailID_hash_code = make_password(code)
                user.emailcode_expires_dt = expiry
                user.save()

            self.send_email(login, code)

        else:  # phone
            user, created = User.objects.get_or_create(
                phoneNumber=login,
                defaults={
                    "phoneNumber_hash_code": code,
                    "phonenumbercode_expires_dt": expiry,
                },
            )

            if not created:
                user.phoneNumber_hash_code = make_password(code)
                user.phonenumbercode_expires_dt = expiry
                user.save()

            # 👉 Here you can integrate SMS API (Twilio, Fast2SMS, etc.)

        return user

    def send_email(self, login, code):

        subject = "Jimiboard Login Code"

        html_message = render_to_string(
            "email/mail_design.html",
            {
                "code": code,
            },
        )

        plain_message = strip_tags(html_message)

        # message = f"Your login verification code is: {code}"
        to = [login]
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [login],
            html_message=html_message,
            fail_silently=False,
        )
