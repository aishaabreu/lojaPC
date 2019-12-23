from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Computador, ComputadorMemoria
from .serializers import (
    ComputadorSerializer,
    UserSerializer,
    ComputadorMemoriaSerializer,
    ComputadorVerboseSerializer)


class ComputadorMemoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComputadorMemoria.objects.all()
    serializer_class = ComputadorMemoriaSerializer


class ComputadorViewSet(viewsets.ModelViewSet):
    queryset = Computador.objects.all()
    serializer_class = ComputadorSerializer

    @action(('GET',), detail=False)
    def verbose(self, request):
        serializer = ComputadorVerboseSerializer(
            self.get_queryset(), many=True)
        
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
