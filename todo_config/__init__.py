from .celery import app as celery_app
# Инициализация Celery-приложения при запуске Django
# Экспорт Celery-приложения, чтобы оно было доступно по имени 'celery_app'
__all__ = ['celery_app']