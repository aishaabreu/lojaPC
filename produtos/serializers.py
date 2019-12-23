from rest_framework import serializers
from .models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo


class ProcessadorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Processador
        fields = "__all__"


class PlacaMaeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlacaMae
        fields = "__all__"


class MemoriaRamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MemoriaRam
        fields = "__all__"


class PlacaDeVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlacaDeVideo
        fields = "__all__"
