from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import TelegramUser
from .serializers import TelegramUserSerializer


class TelegramUserCreateView(generics.CreateAPIView):
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Проверяем, не подключен ли уже Telegram
        if hasattr(request.user, 'telegram'):
            return Response(
                {'detail': 'Telegram уже подключен к этому аккаунту.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class TelegramUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return TelegramUser.objects.get(user=self.request.user)
        except TelegramUser.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {'detail': 'Telegram не подключен к аккаунту.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {'detail': 'Telegram не подключен к аккаунту.'},
                status=status.HTTP_404_NOT_FOUND
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
