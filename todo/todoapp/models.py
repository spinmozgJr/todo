from django.db import models

# Create your models here.
class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Не выполнено'),
        ('done', 'Выполнено'),
    ]

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='Приоритет')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')

    def __str__(self):
        return self.title