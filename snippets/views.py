from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import status, viewsets, permissions

from .models import Snippet, Tag
from .permissions import IsOwnerOrAdmin
from .serializers import (
    SnippetsOverviewSerializer, UserCreateSerializer
)


User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class SnippetsAPIView(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    
    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        return SnippetsOverviewSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"count": len(serializer.data), "data": serializer.data})
