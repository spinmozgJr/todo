"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

from todoapp.views import TodoViewSet, ExportTodosView, TaskStatusView

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/drf-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/v1/logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    # path('api/logout/', LogoutView.as_view()),
    path("api/", include("todoapp.urls")),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)