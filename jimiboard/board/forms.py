import re
import random
from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()

    def validate_login(self, value):
        value = value.strip()

        # Email pattern
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        # Phone pattern (India + international)
        phone_pattern = r"^\+?\d{8,15}$"

        if re.match(email_pattern, value):
            self.context["login_type"] = "email"
            return value

        if re.match(phone_pattern, value):
            self.context["login_type"] = "phone"
            return value

        raise serializers.ValidationError("Enter a valid Email ID or Phone number")

    def create(self, validated_data):
        login = validated_data["login"]
        login_type = self.context["login_type"]

        # Generate OTP / Code
        code = str(random.randint(100000, 999999))

        if login_type == "email":
            user, created = User.objects.get_or_create(
                emailID=login, defaults={"emailID_code": code}
            )
            if not created:
                user.emailID_code = code
                user.save()

            # 👉 Send email here
            # send_email_otp(login, code)

        else:
            user, created = User.objects.get_or_create(
                phone_number=login, defaults={"phone_number_code": code}
            )
            if not created:
                user.phone_number_code = code
                user.save()

            # 👉 Send SMS here
            # send_sms_otp(login, code)

        return user
