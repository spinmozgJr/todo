from celery.result import AsyncResult
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import generics, viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from .models import Todo
from .permissions import IsOwnerOrAdmin
from .serializers import TodoSerializer
from .tasks import export_user_todos_to_csv

class TodoViewSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = TodoSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Todo.objects.all()
        else:
            queryset = Todo.objects.filter(user=user)

        status_param = self.request.query_params.get('status')
        priority_param = self.request.query_params.get('priority')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if priority_param:
            queryset = queryset.filter(priority=priority_param)

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Задача '{instance.title}' успешно удалена."},
            status=status.HTTP_200_OK
        )

# class LogoutView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response({"detail": "Вы вышли из системы."})


class ExportTodosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = export_user_todos_to_csv.delay(request.user.id)
        return Response({
            "task_id": task.id,
            "status_url": f"/api/tasks/{task.id}/"
        })


class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.successful():
            return Response({
                "status": "completed",
                "download_url": request.build_absolute_uri(result.result)
            })
        return Response({"status": result.status.lower()})
