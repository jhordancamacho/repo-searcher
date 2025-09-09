from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializer import UserSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
# class AuthView(APIView):
# 	def post(self, request):
# 		try:
# 			return
# 		except Exception:
# 			return


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
