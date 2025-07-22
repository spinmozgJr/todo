from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer


# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    # queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        queryset = Todo.objects.all()
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


