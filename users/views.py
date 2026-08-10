from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Контроллер списка пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterView(generics.CreateAPIView):
    """Контроллер регистрации нового пользователя."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Проверяем, что пароли совпадают и пароль сложный
        user = serializer.save()
        # Создаем пользователя в БД (пароль хешируется через create_user)
        refresh = RefreshToken.for_user(user)
        # Генерируем токены для этого пользователя
        return Response(
            {
                "user": UserSerializer(
                    user
                ).data,  # Возвращаем данные пользователя (без пароля)
                "refresh": str(refresh),  # Токен обновления (хранится в безопасности)
                "access": str(
                    refresh.access_token
                ),  # Токен доступа (передается в заголовках API)
            },
            status=status.HTTP_201_CREATED,
        )  # Код 201 = Объект успешно создан
