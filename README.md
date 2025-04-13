# TMS_TODO_app
# To-Do App with Celery Reminders

Веб-приложение для управления списком задач с напоминаниями, повторяющимися задачами и аналитикой.

## Функциональность

- Регистрация и вход пользователей
- Создание, редактирование и удаление задач
- Отметка задач как выполненные / снятие выполнения
- Фильтрация задач по категории и приоритету
- Категории и приоритеты задач
- Повторяющиеся задачи (ежедневно, еженедельно, ежемесячно)
- Повторяющиеся задачи создаются автоматически через Celery Beat
- Email-напоминания (за 1 час до дедлайна) через Celery + Redis
- Админ-панель для категорий (доступ только для staff-пользователей)
- REST API с авторизацией (Token, Session)
- Swagger и Redoc-документация API
- Аналитика задач: общее количество, выполненные, просроченные, завершённые за 7 дней


## Технологии

- Python 3.12
- Django 5.2
- PostgreSQL
- Celery + Redis
- Django REST Framework
- django-celery-beat
- drf-yasg


## Установка

1. Клонировать проект:

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Создать файл .env на основе примера:

```bash
SECRET_KEY='your-django-secret-key'
DEBUG='True'
ALLOWED_HOSTS='127.0.0.1,localhost'

DB_NAME='tododb'
DB_USER='todouser'
DB_PASSWORD='todopass'
DB_HOST='localhost'
DB_PORT='5432'

EMAIL_HOST_USER='your-email@gmail.com'
EMAIL_HOST_PASSWORD='your-app-password'
```

5. Применить миграции и создать суперпользователя:

```bash
python manage.py migrate
python manage.py createsuperuser
```


## Запуск

1. Django сервер:

```bash
python manage.py runserver
```

2. Redis:

```bash
brew services start redis  # или redis-server вручную
```

3. Celery воркер:

```bash
celery -A todo_config worker -l info
```

4. Celery Beat:

```bash
celery -A todo_config beat -l info
```

## API

API доступен по адресу: http://localhost:8000/api/tasks/

## Swagger

Документация доступна по адресу: http://127.0.0.1:8000/swagger/


## Redoc

Документация доступна по адресу: http://127.0.0.1:8000/redoc/


## Аналитика

На странице /stats отображается аналитика по задачам.


## Тесты

```bash
python manage.py test
```