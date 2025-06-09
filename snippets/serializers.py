from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Snippet, Tag


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


class SnippetDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Snippet
        fields = [ "title", "note", "created_at", "updated_at" ]


class TagDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = [ "id", "title", "created_at", "updated_at" ]


class TagSnippetDetailSerializer(serializers.ModelSerializer):
    snippets = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = [ "id", "title", "created_at", "updated_at", "snippets" ]
    
    def get_snippets(self, obj):
        tag_snippets = obj.tags.all()
        return [f"{tag_snippet.title}: {tag_snippet.note[:50]}" for tag_snippet in tag_snippets]


class SnippetCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializerField(required=False)

    class Meta:
        model = Snippet
        fields = ['title', 'note', 'tags']
    
    def create(self, validated_data):
        tag_names = validated_data.pop('tags') if "tags" in validated_data else None
        validated_data["user"] = self.context["user"]
        instance = super().create(validated_data)
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(title=name)
                tags.append(tag)
            instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tags') if "tags" in validated_data else None
        instance = super().update(instance, validated_data)
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(title=name)
                tags.append(tag)
            instance.tags.set(tags)
        return instance
