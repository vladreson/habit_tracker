from celery import shared_task
from django.utils import timezone
import telegram
from django.conf import settings
from habits.models import Habit
from .models import TelegramUser


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках каждую минуту."""
    if not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Telegram bot token not configured")
        return

    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('user')

    if not habits.exists():
        print(f"⏰ No habits found for time {current_time}")
        return

    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    sent_count = 0

    for habit in habits:
        try:
            telegram_user = TelegramUser.objects.get(user=habit.user)
            message = "🔔 Напоминание о привычке!\n\n"
            message += f"💫 {habit.action}\n"
            message += f"🕐 Время: {habit.time}\n"
            message += f"📍 Место: {habit.place}\n"
            message += f"⏱ Время на выполнение: {habit.time_to_complete} сек\n"

            if habit.reward:
                message += f"🎁 Вознаграждение: {habit.reward}\n"
            elif habit.related_habit:
                message += f"🔗 Связанная привычка: {habit.related_habit.action}\n"

            bot.send_message(chat_id=telegram_user.chat_id, text=message)
            sent_count += 1
            print(f"✅ Sent reminder to {habit.user.username}")

        except TelegramUser.DoesNotExist:
            print(f"⚠️ No Telegram user for {habit.user.username}")
            continue
        except telegram.error.TelegramError as e:
            print(f"❌ Telegram error for {habit.user.username}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {habit.user.username}: {e}")

    print(f"📨 Sent {sent_count} reminders at {current_time}")


@shared_task
def send_daily_summary():
    """Отправка ежедневного отчета по привычкам."""
    if not settings.TELEGRAM_BOT_TOKEN:
        return

    today = timezone.now().date()

    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    telegram_users = TelegramUser.objects.select_related('user').all()

    for telegram_user in telegram_users:
        try:
            user_habits = Habit.objects.filter(user=telegram_user.user)
            total_habits = user_habits.count()
            public_habits = user_habits.filter(is_public=True).count()

            message = "📊 Ежедневный отчет по привычкам\n\n"
            message += f"👤 Пользователь: {telegram_user.user.username}\n"
            message += f"📈 Всего привычек: {total_habits}\n"
            message += f"🌐 Публичных привычек: {public_habits}\n"
            message += f"📅 Дата: {today}\n\n"
            message += "💪 Продолжайте работать над своими привычками!"

            bot.send_message(chat_id=telegram_user.chat_id, text=message)
            print(f"✅ Sent daily summary to {telegram_user.user.username}")

        except telegram.error.TelegramError as e:
            print(f"❌ Telegram error for {telegram_user.user.username}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {telegram_user.user.username}: {e}")


@shared_task
def test_celery():
    """Тестовая задача для проверки работы Celery."""
    print("✅ Celery is working correctly!")
    return "Celery test task completed successfully"
