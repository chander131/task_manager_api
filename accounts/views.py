import jwt
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import MongoUser
from .serializers import MongoUserSerializer
from django.http import JsonResponse
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = MongoUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = MongoUser.objects.get(username=username)
    except MongoUser.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    if not user.check_password(password):
        return Response(
            {"error": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED
        )

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

    response = JsonResponse(
        {
            "message": "Login exitoso",
            "result": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
        }
    )

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=1800,
        path="/",
        domain=".task-manager.click",
    )
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_user(request):
    response = JsonResponse({"message": "Logout exitoso"})
    response.delete_cookie(key="token", path="/", domain=".task-manager.click")
    return response


@api_view(["GET"])
def current_user(request):
    user = request.user
    return Response(
        {"id": str(user.id), "username": user.username, "email": user.email}
    )
