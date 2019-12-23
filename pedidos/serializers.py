from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import empty
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


class ComputadorVerboseSerializer(serializers.ModelSerializer):
    memoria = serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()
    processador = serializers.SerializerMethodField()
    placa_mae = serializers.SerializerMethodField()
    placa_video = serializers.SerializerMethodField()

    class Meta:
        model = Computador
        fields = "__all__"

    def get_memoria(self, obj):
        return [str(mem) for mem in obj.memoria.all()]

    def get_cliente(self, obj):
        return str(obj.cliente)

    def get_processador(self, obj):
        return str(obj.processador)

    def get_placa_mae(self, obj):
        return str(obj.placa_mae)

    def get_placa_video(self, obj):
        return str(obj.placa_video)


class ComputadorSerializer(serializers.HyperlinkedModelSerializer):
    memoria = ComputadorMemoriaSerializer(many=True)

    class Meta:
        model = Computador
        fields = "__all__"

    def memoria_validation(self, memoria, placa_mae):
        """
            Validação das Memórias no Computador            
            verifica as regras de negócio:
                Deve haver sem uma memória RAM
                Não ultrapassar limite dos slots de memória da placa mãe
                Não ultrapassar limite de memória da placa mãe
        """
        if not memoria:
            raise ValidationError({"memoria": ERRO_MEMORIA_OBRIGATORIA})
        if len(memoria) > placa_mae.slots_memoria:
            raise ValidationError({"memoria": ERRO_SLOTS_MEMORIA})
        total_memoria = 0
        for mem in memoria:
            total_memoria += mem["memoria"].tamanho
        if total_memoria > placa_mae.memoria_suportaca:
            raise ValidationError({"memoria": ERRO_LIMITE_MEMORIA})

    def placa_mae_validation(self, processador, placa_mae):
        if processador and placa_mae and not placa_mae.processadores_suportados.filter(pk=processador.pk).exists():
            raise ValidationError({"placa_mae": ERRO_PLACA_MAE_INCOMPATIVEL})

    def placa_video_validation(self, placa_mae, placa_video):
        if placa_mae and not placa_mae.video_integrado and not placa_video:
            raise ValidationError({"placa_mae": ERRO_PLACA_VIDEO_OBRIGATORIA})

    def computador_validation(self, validated_data, instance=None):
        processador = validated_data.get('processador', instance and instance.processador)
        placa_mae = validated_data.get('placa_mae', instance and instance.placa_mae)
        placa_video = validated_data.get('placa_video', instance and instance.placa_video)

        self.placa_mae_validation(processador, placa_mae)
        self.placa_video_validation(placa_mae, placa_video)

    def save_memoria(self, instance, memoria):
        """
            Salva as memórias de um computador montado
        """
        pk_list = []
        for mem in memoria:
            # Cria cada memória passada pela API
            mem.update({"computador": instance})
            obj = ComputadorMemoria.objects.create(**mem)
            pk_list.append(obj.pk)

        # Remove as memórias que não são mais utilizadas
        ComputadorMemoria.objects.filter(
            computador=instance).exclude(pk__in=pk_list).delete()

    def create(self, validated_data):
        memoria = validated_data.pop("memoria", None)
        placa_mae = validated_data.get('placa_mae', None)

        self.memoria_validation(memoria, placa_mae)
        self.computador_validation(validated_data)

        instance = super().create(validated_data)
        self.save_memoria(instance, memoria)
        return instance

    def update(self, instance, validated_data):
        memoria = validated_data.pop("memoria", empty)

        if memoria is not empty:
            placa_mae = validated_data.get(
                'placa_mae', instance and instance.placa_mae)
            self.memoria_validation(memoria, placa_mae)
        self.computador_validation(validated_data)

        instance = super().update(instance, validated_data)
        if memoria is not empty:
            self.save_memoria(instance, memoria)
        return instance
