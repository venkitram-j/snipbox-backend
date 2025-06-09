from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from .serializers import UserCreateSerializer


User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer