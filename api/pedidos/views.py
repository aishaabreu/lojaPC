from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Computador, ComputadorMemoria
from .serializers import ComputadorSerializer, UserSerializer, ComputadorMemoriaSerializer


class ComputadorMemoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComputadorMemoria.objects.all()
    serializer_class = ComputadorMemoriaSerializer


class ComputadorViewSet(viewsets.ModelViewSet):
    queryset = Computador.objects.all()
    serializer_class = ComputadorSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
