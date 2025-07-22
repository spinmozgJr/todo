from rest_framework import serializers
from django.utils import timezone

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Дедлайн не может быть в прошлом')
        return value

    def validate_status(self, value):
        if self.instance is None and value == 'done':
            raise serializers.ValidationError("Нельзя создать задачу со статусом 'Выполнено'")
        return value