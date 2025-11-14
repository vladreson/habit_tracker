from django.core.exceptions import ValidationError


def validate_time_to_complete(value):
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд.')


def validate_related_habit(value):
    if value and not value.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной.')


def validate_pleasant_habit(instance):
    if instance.is_pleasant:
        if instance.reward:
            raise ValidationError({'reward': 'У приятной привычки не может быть вознаграждения.'})
        if instance.related_habit:
            raise ValidationError(
                {'related_habit': 'У приятной привычки не может быть связанной привычки.'}
            )
