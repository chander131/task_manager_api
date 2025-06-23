# authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import os
from .models import MongoUser

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class MongoUserJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("token")

        if not token:
            return None

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expirado")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token inválido")

        try:
            user = MongoUser.objects.get(id=payload["sub"])
        except MongoUser.DoesNotExist:
            raise AuthenticationFailed("Usuario no encontrado")

        return (user, None)
