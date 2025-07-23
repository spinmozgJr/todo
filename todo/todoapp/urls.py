from django.urls import path
from .views import ExportTodosView, TaskStatusView

urlpatterns = [
    path("todos/export/", ExportTodosView.as_view()),
    path("tasks/<str:task_id>/", TaskStatusView.as_view()),
]
