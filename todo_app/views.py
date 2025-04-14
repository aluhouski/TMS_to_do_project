from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task, Category
from .forms import TaskForm, CategoryForm, UserRegisterForm
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer, CategorySerializer

from django_filters.rest_framework import DjangoFilterBackend



# Django views
# Главная страница со списком задач
@login_required
def task_list(request):
    # Получаем параметры фильтрации из GET-запроса
    category_id = request.GET.get('category', '').strip()
    priority = request.GET.get('priority', '').strip()

    # Показываем только задачи текущего пользователя
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    # Фильтрация по категории (если указана)
    if category_id and category_id.isdigit():
        tasks = tasks.filter(category__id=int(category_id))

    # Фильтрация по приоритету (если указан)
    if priority:
        tasks = tasks.filter(priority=priority)

    categories = Category.objects.all()

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'categories': categories,
        'selected_category': category_id,
        'selected_priority': priority
    })


# Просмотр деталей задачи
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


# Создание новой задачи
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            if task.is_completed:
                task.closed_at = timezone.now()
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


# Обновление существующей задачи/установка даты выполнения
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    old_status = task.is_completed

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)

            # Если задача только что была выполнена
            if not old_status and updated_task.is_completed:
                updated_task.closed_at = timezone.now()

            # Если сняли выполнение — обнуляем closed_at
            if old_status and not updated_task.is_completed:
                updated_task.closed_at = None

            updated_task.save()
            return redirect('task_list')
    else:
        # Если GET-запрос — отображаем форму с текущими данными задачи
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form})


# Удаление задачи
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')


# Отображение статистики по задачам
@login_required
def task_stats(request):
    user = request.user  
    now = timezone.now() 

    # Общее кол-во задач пользователя
    total_tasks = Task.objects.filter(user=user).count()

    # Кол-во выполненных задач
    completed_tasks = Task.objects.filter(user=user, is_completed=True).count()

    # Кол-во просроченных задач
    overdue_tasks = Task.objects.filter(
        user=user,
        is_completed=False,
        due_date__lt=now
    ).count()

    # Кол-во задач, завершённых за последние 7 дней
    recent_completed = Task.objects.filter(
        user=user,
        is_completed=True,
        closed_at__gte=now - timedelta(days=7)
    ).count()

    return render(request, 'tasks/task_stats.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_completed': recent_completed,
    })


# Список всех категорий
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'tasks/category_list.html', {'categories': categories})


# Проверка пользователя: админ или нет
def is_admin(user):
    return user.is_staff


# Создание новой категории (только для админов)
@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'tasks/category_form.html', {'form': form})


# Обновление существующей категории (только для админов)
@user_passes_test(is_admin)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        # Если GET-запрос — отображаем форму с текущими данными категории
        form = CategoryForm(instance=category)

    return render(request, 'tasks/category_form.html', {'form': form})


# Удаление категории (только для админов)
@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('category_list')


# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})



# DRF ViewSets
# API endpoint для задач
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['priority', 'category', 'is_completed']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # Присваиваем пользователя при создании задачи
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# API endpoint для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]