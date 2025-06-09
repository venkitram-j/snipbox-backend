"""
URL configuration for snipbox project.

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
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from snippets.views import SnippetsAPIView, TagAPIView, UserCreateAPIView


router = routers.DefaultRouter()
router.register(r'tags', TagAPIView, basename='tags')
router.register(r'snippets', SnippetsAPIView, basename='snippets')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    
    path(f'{settings.API_ROOT_URL}/auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path(f'{settings.API_ROOT_URL}/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path(f'{settings.API_ROOT_URL}/users/', UserCreateAPIView.as_view(), name='user-create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
