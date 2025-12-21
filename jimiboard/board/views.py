from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import LoginSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Verification code sent successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
def Index(request):
    return render(request, "Index.html")


def SignUp(request):
    return render(request, "registration.html")
