from django.test import TestCase
from django.core.exceptions import ValidationError
from habits.validators import validate_time_to_complete, validate_related_habit
from habits.models import Habit
from django.contrib.auth import get_user_model

User = get_user_model()


class ValidatorsTest(TestCase):
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
        self.useful_habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Бегать',
            time_to_complete=60
        )

    def test_validate_time_to_complete_valid(self):
        try:
            validate_time_to_complete(120)
        except ValidationError:
            self.fail("validate_time_to_complete raised ValidationError unexpectedly")

    def test_validate_time_to_complete_invalid(self):
        with self.assertRaises(ValidationError):
            validate_time_to_complete(121)

    def test_validate_related_habit_valid(self):
        try:
            validate_related_habit(self.pleasant_habit)
        except ValidationError:
            self.fail("validate_related_habit raised ValidationError unexpectedly")

    def test_validate_related_habit_invalid(self):
        with self.assertRaises(ValidationError):
            validate_related_habit(self.useful_habit)
