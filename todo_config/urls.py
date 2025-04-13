from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Конфиг для Swagger / ReDoc документации
schema_view = get_schema_view(
    openapi.Info(
        title='To-Do List API',
        default_version='v1',
        description='Документация API для приложения управления задачами.',
        terms_of_service='https://example.com/terms/',
        contact=openapi.Contact(email='tmstodoapp@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Django маршруты (todo_app)
    path('', include('todo_app.urls')),

    # Login/Logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Swagger/ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]