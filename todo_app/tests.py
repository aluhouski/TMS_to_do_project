from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework.test import APIClient
from .models import Task, Category
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse



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


# Тест для модели Category
class CategoryPermissionsTest(TestCase):
    # Создаём админа и обычного пользователя
    def setUp(self):
        self.admin_user = User.objects.create_user(username='AdminUser', password='Apass123', is_staff=True)
        self.regular_user = User.objects.create_user(username='RegularUser', password='Upass456')

        self.client = Client()

    # Админ создает категорию
    def test_admin_can_create_category(self):
        self.client.login(username='AdminUser', password='Apass123')
        response = self.client.post(reverse('category_create'), {
            'name': 'Можно',
            'color': '#123456'
        })
        self.assertEqual(response.status_code, 302)  # редирект после успешного создания
        self.assertTrue(Category.objects.filter(name='Можно').exists())

    # Простой юзер создает категорию
    def test_regular_user_cannot_create_category(self):
        self.client.login(username='RegularUser', password='Upass456')
        response = self.client.post(reverse('category_create'), {
            'name': 'Нельзя',
            'color': '#FF0000'
        })
        self.assertEqual(response.status_code, 403)  # доступ запрещён
        self.assertFalse(Category.objects.filter(name='Нельзя').exists())



# Тесты для API
class TaskAPITestCase(TestCase):
    # Создаём пользователя, категорию и тестовую задачу
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='ApiUser', password='Apass890')
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
        self.client.login(username='ApiUser', password='Apass890')
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DRF API Task')           # Проверка наличия заголовка в ответе

    # Неавторизованный пользователь получает отказ (401)
    def test_task_detail_unauthenticated(self):
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 401)