from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Computador, ComputadorMemoria
from .forms import (ERRO_MEMORIA_OBRIGATORIA,
    ERRO_SLOTS_MEMORIA,
    ERRO_LIMITE_MEMORIA,
    ERRO_PLACA_MAE_INCOMPATIVEL,
    ERRO_PLACA_VIDEO_OBRIGATORIA,)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("url", "username", "first_name", "last_name", "email",)


class ComputadorMemoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComputadorMemoria
        fields = ("url", "memoria",)


class ComputadorSerializer(serializers.HyperlinkedModelSerializer):
    memoria = ComputadorMemoriaSerializer(many=True)

    class Meta:
        model = Computador
        fields = "__all__"

    def memoria_validation(self, memoria, instance=None):
        pass

    def placa_mae_validation(self, processador, placa_mae):
        if not placa_mae.processadores_suportados.filter(pk=processador.pk).exists():
            raise ValidationError({"placa_mae": ERRO_PLACA_MAE_INCOMPATIVEL})

    def create(self, validated_data):
        memoria = validated_data.pop("memoria")
        processador = validated_data.get('processador', None)
        placa_mae = validated_data.get('placa_mae', None)
        self.memoria_validation(memoria)
        self.placa_mae_validation(processador, placa_mae)

        instance = super().create(validated_data)
        for mem in memoria:
            mem.update({"computador": instance})
            ComputadorMemoria.objects.create(**mem)
        return instance

    def update(self, instance, validated_data):
        memoria = validated_data.pop("memoria")
        self.memoria_validation(memoria, instance)
        return super().update(instance, validated_data)
