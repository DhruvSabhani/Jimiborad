from django.shortcuts import render, redirect
from .forms import LoginSerializer


# Create your views here.
def Index(request):
    return render(request, "Index.html")


def SignUp(request):
    error = ""
    show_otp = False
    login_value = ""

    if request.method == "POST":
        login_value = request.POST.get("mORem")
        serializer = LoginSerializer(data={"login": login_value})

        if serializer.is_valid():
            serializer.save()
            show_otp = True
        else:
            error = "Invalid Email ID or Phone number"

    return render(
        request,
        "registration.html",
        {"error": error, "show_otp": show_otp, "login_value": login_value},
    )

    # return render(request, "registration.html")
