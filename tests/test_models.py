from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from habits.models import Habit
from telegram_bot.models import TelegramUser

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(username='testuser')
        self.assertEqual(str(user), 'testuser')


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Читать книгу',
            time_to_complete=120
        )
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, 'Дом')
        self.assertEqual(habit.action, 'Читать книгу')
        self.assertEqual(habit.time_to_complete, 120)
        self.assertFalse(habit.is_pleasant)
        self.assertFalse(habit.is_public)

    def test_habit_str(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Бегать',
            time_to_complete=60
        )
        expected_str = f"Я буду Бегать в 08:00:00 в Парк"
        self.assertEqual(str(habit), expected_str)

    def test_habit_validation_time_exceeded(self):
        habit = Habit(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Читать книгу',
            time_to_complete=121
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_with_reward_validation(self):
        habit = Habit(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Слушать музыку',
            is_pleasant=True,
            reward='Конфета',
            time_to_complete=60
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_with_both_related_and_reward_validation(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Слушать музыку',
            is_pleasant=True,
            time_to_complete=60
        )

        habit = Habit(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Бегать',
            related_habit=pleasant_habit,
            reward='Конфета',
            time_to_complete=60
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


class TelegramUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_telegram_user(self):
        telegram_user = TelegramUser.objects.create(
            user=self.user,
            chat_id=123456789,
            username='testuser_tg'
        )
        self.assertEqual(telegram_user.user, self.user)
        self.assertEqual(telegram_user.chat_id, 123456789)
        self.assertEqual(telegram_user.username, 'testuser_tg')

    def test_telegram_user_str(self):
        telegram_user = TelegramUser.objects.create(
            user=self.user,
            chat_id=123456789
        )
        expected_str = f"{self.user.username} (123456789)"
        self.assertEqual(str(telegram_user), expected_str)
