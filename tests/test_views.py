from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit
from telegram_bot.models import TelegramUser

User = get_user_model()


class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )

    def test_user_registration(self):
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_registration_invalid_data(self):
        url = reverse('user-register')
        invalid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token(self):
        url = reverse('api-token-auth')
        data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_user_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')

    def test_get_user_profile_unauthenticated(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HabitAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Читать книгу',
            time_to_complete=60
        )
        self.public_habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Бегать',
            time_to_complete=30,
            is_public=True
        )

    def test_create_habit_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        data = {
            'place': 'Офис',
            'time': '10:00:00',
            'action': 'Работать',
            'time_to_complete': 90
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_create_habit_unauthenticated(self):
        url = reverse('habits-list')
        data = {
            'place': 'Офис',
            'time': '10:00:00',
            'action': 'Работать',
            'time_to_complete': 90
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_habit_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-detail', kwargs={'pk': self.habit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Читать книгу')

    def test_retrieve_habit_not_owner(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('habits-detail', kwargs={'pk': self.habit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_list(self):
        url = reverse('habits-public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_habit_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-detail', kwargs={'pk': self.habit.id})
        data = {'action': 'Читать газету'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Читать газету')

    def test_delete_habit_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-detail', kwargs={'pk': self.habit.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)


class TelegramBotAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_connect_telegram_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('telegram-connect')
        data = {
            'chat_id': 123456789,
            'username': 'testuser_tg'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TelegramUser.objects.count(), 1)

    def test_connect_telegram_duplicate(self):
        TelegramUser.objects.create(
            user=self.user,
            chat_id=123456789
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('telegram-connect')
        data = {
            'chat_id': 987654321,
            'username': 'testuser_tg2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_telegram_info_authenticated(self):
        telegram_user = TelegramUser.objects.create(
            user=self.user,
            chat_id=123456789
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('telegram-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_id'], 123456789)

    def test_get_telegram_info_not_connected(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('telegram-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_telegram_connection(self):
        telegram_user = TelegramUser.objects.create(
            user=self.user,
            chat_id=123456789
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('telegram-me')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TelegramUser.objects.count(), 0)
