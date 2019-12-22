from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Computador, ComputadorMemoria


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("url", "username", "first_name", "last_name", "email",)


class ComputadorMemoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputadorMemoria
        fields = ("id", "memoria",)


class ComputadorSerializer(serializers.HyperlinkedModelSerializer):
    memoria = ComputadorMemoriaSerializer(many=True)

    class Meta:
        model = Computador
        fields = "__all__"
