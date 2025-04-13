from django.contrib import admin
from .models import Task, Category



# Пользовательское действие: отметить задачи как выполненные
@admin.action(description='Отметить как выполненные')
def mark_as_completed(modeladmin, request, queryset):
    queryset.update(is_completed=True)


# Пользовательское действие: снять отметку о выполнении
@admin.action(description='Снять отметку о выполнении')
def unmark_completed(modeladmin, request, queryset):
    queryset.update(is_completed=False)


# Модель Task: отображение в админке
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'short_description', 'created_at', 'due_date', 'priority', 'is_completed', 'closed_at', 'repeat')
    list_filter = ('is_completed', 'priority', 'due_date', 'category', 'closed_at', 'created_at',)
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-due_date',)
    actions = [mark_as_completed, unmark_completed]

    # Сокращаем отображение описания задачи
    def short_description(self, obj):
        if obj.description and len(obj.description) > 40:
            return obj.description[:40] + '...'
        return obj.description or '-'
    
    short_description.short_description = 'Описание'


# Модель Category: отображение в админке
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Регистрация моделей в админке
admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)