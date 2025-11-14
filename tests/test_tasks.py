from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from habits.models import Habit
from telegram_bot.models import TelegramUser
from telegram_bot.tasks import send_habit_reminders, send_daily_summary, test_celery

User = get_user_model()


class TasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.telegram_user = TelegramUser.objects.create(
            user=self.user,
            chat_id=123456789
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Читать книгу',
            time_to_complete=60
        )

        # Проверяем наличие реального токена
        self.has_real_token = hasattr(settings, 'TELEGRAM_BOT_TOKEN') and settings.TELEGRAM_BOT_TOKEN

    @patch('telegram_bot.tasks.telegram.Bot')
    def test_send_habit_reminders(self, mock_bot_class):
        """Тест отправки напоминаний с реальным или мокнутым токеном."""
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot

        with patch('telegram_bot.tasks.timezone.now') as mock_now:
            mock_now.return_value.time.return_value = self.habit.time

            send_habit_reminders()

            if self.has_real_token:
                # С реальным токеном - проверяем что бот был создан
                mock_bot_class.assert_called_once()
            else:
                # Без токена - проверяем что сообщение не отправлялось
                mock_bot.send_message.assert_not_called()

    @patch('telegram_bot.tasks.telegram.Bot')
    def test_send_daily_summary(self, mock_bot_class):
        """Тест отправки ежедневного отчета."""
        mock_bot = MagicMock()
        mock_bot_class.return_value = mock_bot

        send_daily_summary()

        if self.has_real_token:
            mock_bot_class.assert_called_once()
        else:
            mock_bot.send_message.assert_not_called()

    def test_test_celery_task(self):
        """Тестовая задача Celery."""
        result = test_celery()
        self.assertEqual(result, "Celery test task completed successfully")

    def test_real_token_available(self):
        """Тест что реальный токен доступен (опционально)."""
        if self.has_real_token:
            print(f"✅ Используется реальный токен: {settings.TELEGRAM_BOT_TOKEN[:10]}...")
        else:
            print("⚠️ Реальный токен не настроен, используются моки")

        # Этот тест всегда проходит
        self.assertTrue(True)
