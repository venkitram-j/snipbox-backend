from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import status, viewsets, permissions

from .models import Snippet, Tag
from .permissions import IsOwnerOrAdmin
from .serializers import (
    SnippetsOverviewSerializer, SnippetDetailSerializer, UserCreateSerializer, 
    SnippetCreateSerializer, TagDetailSerializer, TagSnippetDetailSerializer
)


User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class SnippetsAPIView(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    
    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in [ "retrieve", "update", "destroy" ]:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in [ "retrieve" ]:
            return SnippetDetailSerializer
        elif self.action in [ "create", "update" ]:
            return SnippetCreateSerializer
        return SnippetsOverviewSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"count": len(serializer.data), "data": serializer.data})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        updated_instance = Snippet.objects.get(id=instance.id)
        updated_serializer = SnippetDetailSerializer(updated_instance)
        return Response(updated_serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [ permissions.IsAuthenticated ]
    
    def get_serializer_class(self):
        if self.action in [ "list" ]:
            return TagDetailSerializer
        elif self.action in [ "retrieve" ]:
            return TagSnippetDetailSerializer
        return TagDetailSerializer
