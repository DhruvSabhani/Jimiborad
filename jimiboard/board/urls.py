from django.contrib import admin
from django.urls import path, include
from board import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.Index, name="Home Page"),
    path("login/", views.SignUp, name="Registration Page"),
    # path("mail", views.mail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
