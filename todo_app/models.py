from django.db import models
from django.contrib.auth.models import User



# Модель Категорий задач
class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#808080') # HEX-формат

    def __str__(self):
        return self.name
    
    # Название во множественном числе для админки
    class Meta:
        verbose_name_plural = 'Categories'


# Варианты приоритета
PRIORITY_CHOICES = [
    ('low', 'низкий'),
    ('medium', 'средний'),
    ('high', 'высокий'),
]


# Варианты повторения задач
REPEAT_CHOICES = [
    ('none', 'не повторять'),
    ('daily', 'ежедневно'),
    ('weekly', 'еженедельно'),
    ('monthly', 'ежемесячно'),
]


# Модель Задач
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')

    def __str__(self):
        return self.title