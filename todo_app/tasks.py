from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task
from django.core.mail import send_mail



# Повторяющиеся задачи
@shared_task
def create_repeated_tasks():
    """
    Проверяет завершённые задачи с установленным повторением (ежедневно, еженедельно, ежемесячно),
    и создает новые копии с новой датой дедлайна.
    """
    # Берём только выполненные задачи, срок которых уже наступил
    now = timezone.now()
    tasks = Task.objects.filter(repeat__in=['daily', 'weekly', 'monthly'], 
                                is_completed=True, due_date__lte=now)

    # Определяем следующий дедлайн в зависимости от типа повторения
    for task in tasks:
        if task.repeat == 'daily':
            next_due = task.due_date + timedelta(days=1)
        elif task.repeat == 'weekly':
            next_due = task.due_date + timedelta(weeks=1)
        elif task.repeat == 'monthly':
            next_due = task.due_date + timedelta(days=30)
        else:
            continue

        # Защита от дублей
        if Task.objects.filter(user=task.user, title=task.title, due_date=next_due).exists():
            continue

        # Создаем новую задачу с теми же данными, но новым дедлайном
        Task.objects.create(
            user=task.user,
            title=task.title,
            description=task.description,
            due_date=next_due,
            category=task.category,
            priority=task.priority,
            repeat=task.repeat
        )


# Отправка email-напоминаний
def send_reminder_email(user_email, task_title, task_due):
    """
    Отправляет письмо-напоминание о задаче на email пользователя.
    """
    subject = f'Напоминание: время выполнения задачи "{task_title}" скоро истекает'
    message = (
        f'Привет!\n'
        f'Не забудь: задача "{task_title}" должна быть выполнена до дедлайна: {task_due}.'
    )
    from_email = 'tmstodoapp@gmail.com'

    send_mail(subject, message, from_email, [user_email])


@shared_task
def send_task_reminders():
    """
    Ищет задачи, срок выполнения которых наступит в течение часа,
    и отправляет уведомление пользователю по email.
    """
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)

    # Только невыполненные задачи с дедлайном в течение часа
    tasks = Task.objects.filter(
        is_completed=False,
        due_date__gte=now,
        due_date__lte=one_hour_later
    )

    for task in tasks:
        user = task.user
        if user.email:
            send_reminder_email(user.email, task.title, task.due_date)