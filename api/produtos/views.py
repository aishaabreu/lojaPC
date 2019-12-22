from rest_framework import viewsets
from .models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo
from .serializers import ProcessadorSerializer, PlacaMaeSerializer, MemoriaRamSerializer, PlacaDeVideoSerializer


class ProcessadorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Processador.objects.all()
    serializer_class = ProcessadorSerializer


class PlacaMaeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlacaMae.objects.all()
    serializer_class = PlacaMaeSerializer


class MemoriaRamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemoriaRam.objects.all()
    serializer_class = MemoriaRamSerializer


class PlacaDeVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlacaDeVideo.objects.all()
    serializer_class = PlacaDeVideoSerializer
