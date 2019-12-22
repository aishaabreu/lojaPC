from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Computador
from .serializers import ComputadorSerializer, UserSerializer


class ComputadorViewSet(viewsets.ModelViewSet):
    queryset = Computador.objects.all()
    serializer_class = ComputadorSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
