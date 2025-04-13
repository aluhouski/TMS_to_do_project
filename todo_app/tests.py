from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Task, Category
from django.utils import timezone
from datetime import timedelta



# Тесты для модели Task
class TaskModelTest(TestCase):
    # Создаём пользователя и категорию для использования в тестах
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='Tpass123')
        self.category = Category.objects.create(name='Работа', color='#1E90FF')

    # Проверяем, что задача создаётся с нужными значениями
    def test_create_task(self):
        task = Task.objects.create(
            user=self.user,
            title='Проверка',
            description='Описание задачи',
            due_date=timezone.now() + timedelta(days=1),
            category=self.category,
            priority='high'
        )
        self.assertEqual(task.title, 'Проверка')        # Проверка заголовка
        self.assertFalse(task.is_completed)             # Новая задача по умолчанию не выполнена
        self.assertEqual(task.category.name, 'Работа')  # Категория совпадает


# Тесты для модели Category
class CategoryModelTest(TestCase):
    # Проверка метода __str__, должен возвращать название категории
    def test_category_str(self):
        category = Category.objects.create(name='Тест', color='#FFFF00')
        self.assertEqual(str(category), 'Тест')



# Тесты для API
class TaskAPITestCase(TestCase):
    # Создаём пользователя, категорию и тестовую задачу
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Учёба', color='#FFD700')
        self.task = Task.objects.create(
            user=self.user,
            title='DRF API Task',
            description='Описание задачи через API',
            category=self.category,
            priority='medium',
        )

    # Авторизованный пользователь получает доступ к задаче
    def test_task_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DRF API Task')           # Проверка наличия заголовка в ответе

    # Неавторизованный пользователь получает отказ (401)
    def test_task_detail_unauthenticated(self):
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 401)