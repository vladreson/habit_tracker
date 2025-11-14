from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_time_to_complete,
    validate_related_habit,
    validate_pleasant_habit,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'frequency', 'reward', 'time_to_complete',
            'is_public', 'created_at',
        ]
        read_only_fields = ['user', 'created_at']

    def validate_time_to_complete(self, value):
        validate_time_to_complete(value)
        return value

    def validate_related_habit(self, value):
        if value:
            validate_related_habit(value)
        return value

    def validate(self, data):
        instance = Habit(**data)
        validate_pleasant_habit(instance)

        related_habit = data.get('related_habit')
        reward = data.get('reward', '')

        if related_habit and reward:
            raise serializers.ValidationError({
                'reward': 'Нельзя одновременно выбирать связанную привычку и вознаграждение.',
                'related_habit': 'Нельзя одновременно выбирать связанную привычку и вознаграждение.',
            })

        return data
