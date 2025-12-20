from django.shortcuts import render, redirect


# Create your views here.
def Index(request):
    return render(request, "Index.html")


def SignUp(request):
    return render(request, "registration.html")
