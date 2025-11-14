from django.urls import path
from .views import TelegramUserCreateView, TelegramUserDetailView

urlpatterns = [
    path('connect/', TelegramUserCreateView.as_view(), name='telegram-connect'),
    path('me/', TelegramUserDetailView.as_view(), name='telegram-me'),
]
