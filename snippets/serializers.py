from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Snippet


User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TagSerializerField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list('title', flat=True)

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags.")
        return data


class SnippetsOverviewSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    link = serializers.HyperlinkedIdentityField(view_name='snippets-detail', format='html')
    tags = TagSerializerField()
    
    class Meta:
        model = Snippet
        fields = [ "id", "title", "note", "user", "tags", "created_at", "updated_at", "link" ]
