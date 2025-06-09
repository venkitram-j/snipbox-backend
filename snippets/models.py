from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    """
    Abstract base class that adds created_at and updated_at fields to models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(TimeStampedModel):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Snippet(TimeStampedModel):
    title = models.CharField(max_length=200)
    note = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    tags = models.ManyToManyField(Tag, related_name='tags')
    
    def __str__(self):
        return f"{self.title}: {self.note[:50]}"
