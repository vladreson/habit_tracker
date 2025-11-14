from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'time', 'place', 'is_pleasant', 'is_public', 'created_at')
    list_filter = ('is_pleasant', 'is_public', 'frequency', 'created_at')
    search_fields = ('action', 'place', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
