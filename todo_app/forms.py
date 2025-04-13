from django import forms
from .models import Task, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Форма регистрации пользователя с добавлением обязательного поля: email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма создания/редактирования задачи
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 
                  'is_completed', 'category', 'priority', 'repeat']

        # Кастомизация отображения полей
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Название задачи',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Описание (необязательно)',
                'class': 'form-control',
                'rows': 3
            }),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'repeat': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# Форма для создания категории (только для админа)
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']