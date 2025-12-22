from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail


# def mail(request):
#     subject = "Jimiboard"
#     msg = "Congratulations for your success"
#     to = "kano363320@gmail.com"
#     res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
#     if res == 1:
#         msg = "Mail Sent Successfuly"
#     else:
#         msg = "Mail could not sent"
#     return HttpResponse(msg)


# Create your views here.
def Index(request):
    return render(request, "Index.html")


def SignUp(request):
    return render(request, "registration.html")
