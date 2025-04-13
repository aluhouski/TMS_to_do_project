import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_config.settings')


app = Celery('todo_config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Настройка периодического запуска задач (celery beat)
app.conf.beat_schedule = {
# Проверка для создания повторяющихся задач
    'create-repeated-tasks-every-day': {
        'task': 'todo_app.tasks.create_repeated_tasks',
        'schedule': crontab(minute=00, hour=00),  # каждый день в 00:00
    },
# Проверка на отправку напоминаний по email
    'send-task-reminders-every-10min': {
        'task': 'todo_app.tasks.send_task_reminders',
        'schedule': crontab(minute='*/10'),  # каждые 10 минут
    },
}