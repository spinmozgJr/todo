from celery import shared_task
import time

@shared_task
def test_delay():
    time.sleep(2)
    return "CSV export complete"

import csv
import os
from celery import shared_task
from django.conf import settings
from .models import Todo

@shared_task
def export_user_todos_to_csv(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)

    todos = Todo.objects.filter(user=user)

    filename = f"todo_export_{user.id}.csv"
    folder = os.path.join(settings.MEDIA_ROOT, "exports")
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", newline='', encoding='cp1251') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([
            "ID",
            "Заголовок",
            "Описание",
            "Дата создания",
            "Дедлайн",
            "Приоритет",
            "Статус"
        ])
        for todo in todos:
            writer.writerow([
                todo.user,
                todo.title,
                todo.description,
                todo.created_at.strftime("%Y-%m-%d %H:%M"),
                todo.deadline.strftime("%Y-%m-%d %H:%M"),
                todo.get_priority_display(),  # показывает человеко-понятное значение
                todo.get_status_display()  # то же для статуса
            ])

    return f"/media/exports/{filename}"

