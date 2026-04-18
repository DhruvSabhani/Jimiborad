from django.shortcuts import render, redirect
from .forms import LoginSerializer
from .models import User
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.utils import timezone


# Create your views here.
def Index(request):
    return render(request, "Index.html")


def SignUp(request):
    if request.method == "POST":
        login_value = request.POST.get("mORem")
        serializer = LoginSerializer(data={"login": login_value})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({"success": True})

        return JsonResponse(
            {"success": False, "message": "• Invalid Email ID or Phone number"}
        )
    return render(request, "registration.html")


def verify_code(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "• Invalid request"})

    check_email = request.POST.get("check_email")
    check_code = request.POST.get("check_code")

    if not check_email or not check_code:
        return JsonResponse({"success": False, "message": "• Missing data"})

    # 🔍 Find user with valid (not expired) OTP
    user = (
        User.objects.filter(
            emailID=check_email,
            emailcode_expires_dt__gt=timezone.now(),
            emailID_hash_code__isnull=False,
        )
        .only("id", "emailID_hash_code")
        .first()
    )

    # 🔐 Verify OTP
    if (
        not user
        or not user.emailID_hash_code
        or not check_password(check_code, user.emailID_hash_code)
    ):
        return JsonResponse({"success": False, "message": "• Code expired or invalid"})

    # ✅ invalidate OTP after success
    user.save(update_fields=["emailcode_expires_dt"])

    return JsonResponse({"success": True, "message": "• Code verified successfully"})


def my_profile(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "• Invalid request"})

    email = request.POST.get("emailID")
    username = request.POST.get("username")
    user_img = request.FILES.get("userImg")

    user = User.objects.filter(emailID=email).first()

    if not user:
        return JsonResponse({"success": False, "message": "User not found"})

    user.username = username
    user.userImg = user_img
    user.save()

    return JsonResponse({"success": True, "message": "Profile saved"})
