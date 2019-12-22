from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo
from .serializers import ProcessadorSerializer, PlacaMaeSerializer, MemoriaRamSerializer, PlacaDeVideoSerializer


class ProcessadorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Processador.objects.all()
    serializer_class = ProcessadorSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('descricao',)


class PlacaMaeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlacaMae.objects.all()
    serializer_class = PlacaMaeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('processadores_suportados',)
    search_fields = ('descricao',)


class MemoriaRamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemoriaRam.objects.all()
    serializer_class = MemoriaRamSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('descricao', 'tamanho')


class PlacaDeVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlacaDeVideo.objects.all()
    serializer_class = PlacaDeVideoSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('descricao',)
