from rest_framework import serializers
from .models import Task



# Сериализатор для модели Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'