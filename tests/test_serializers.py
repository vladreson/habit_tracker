from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.serializers import HabitSerializer
from users.serializers import UserRegistrationSerializer, UserSerializer
from telegram_bot.serializers import TelegramUserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

    def test_user_registration_serializer_valid(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_registration_serializer_invalid_passwords(self):
        invalid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass'
        }
        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', serializer.errors)

    def test_user_serializer(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['email'], 'test@example.com')


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Слушать музыку',
            is_pleasant=True,
            time_to_complete=60
        )

    def test_habit_serializer_valid(self):
        data = {
            'place': 'Парк',
            'time': '08:00:00',
            'action': 'Бегать',
            'time_to_complete': 60
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_habit_serializer_invalid_time(self):
        data = {
            'place': 'Парк',
            'time': '08:00:00',
            'action': 'Бегать',
            'time_to_complete': 121
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('time_to_complete', serializer.errors)

    def test_habit_serializer_pleasant_with_reward(self):
        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Слушать музыку',
            'is_pleasant': True,
            'reward': 'Конфета',
            'time_to_complete': 60
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reward', serializer.errors)

    def test_habit_serializer_both_related_and_reward(self):
        data = {
            'place': 'Парк',
            'time': '08:00:00',
            'action': 'Бегать',
            'related_habit': self.pleasant_habit.id,
            'reward': 'Конфета',
            'time_to_complete': 60
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reward', serializer.errors)
        self.assertIn('related_habit', serializer.errors)


class TelegramUserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_telegram_user_serializer_valid(self):
        data = {
            'chat_id': 123456789,
            'username': 'testuser_tg'
        }
        serializer = TelegramUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_telegram_user_serializer_missing_chat_id(self):
        data = {
            'username': 'testuser_tg'
        }
        serializer = TelegramUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('chat_id', serializer.errors)
