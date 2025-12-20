from django.contrib import admin
from django.urls import path, include
from board import views

urlpatterns = [
    path("", views.Index, name="Home Page"),
    path("login/", views.SignUp, name="Registration Page"),
]
