from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo_app.views import TaskViewSet
import todo_app.views as views
from rest_framework.authtoken.views import obtain_auth_token



# DRF Router (API-эндпоинты)
router = DefaultRouter()
router.register(r'api/tasks', TaskViewSet, basename='task')


urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Django Views
    path('', views.task_list, name='task_list'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('register/', views.register, name='register'),
    path('stats/', views.task_stats, name='task_stats'),

    # DRF API
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
]