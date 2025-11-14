from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(
        max_length=500,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='daily',
        verbose_name='Периодичность'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вознаграждение'
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name='Время на выполнение (в секундах)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def clean(self):
        errors = {}

        if self.related_habit and self.reward:
            errors['reward'] = 'Нельзя одновременно выбирать связанную привычку и вознаграждение.'

        if self.time_to_complete > 120:
            errors['time_to_complete'] = 'Время выполнения не должно превышать 120 секунд.'

        if self.related_habit and not self.related_habit.is_pleasant:
            errors['related_habit'] = 'Связанная привычка должна быть приятной.'

        if self.is_pleasant:
            if self.reward:
                errors['reward'] = 'У приятной привычки не может быть вознаграждения.'
            if self.related_habit:
                errors['related_habit'] = 'У приятной привычки не может быть связанной привычки.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"
