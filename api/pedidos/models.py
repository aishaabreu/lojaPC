from django.db import models
from django.conf import settings
from django.core.validators import ValidationError
from produtos.models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo


class Computador(models.Model):
    class Meta:
        verbose_name_plural = "Computadores"

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    processador = models.ForeignKey(Processador, on_delete=models.PROTECT)
    placa_mae = models.ForeignKey(
        PlacaMae, verbose_name="Placa Mãe", on_delete=models.PROTECT)
    placa_video = models.ForeignKey(
        PlacaDeVideo, verbose_name="Placa de Vídeo",
        null=True, blank=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return "{cliente} - {processador} ({placa_mae})".format(
            cliente=self.cliente,
            processador=self.processador,
            placa_mae=self.placa_mae,
        )


class ComputadorMemoria(models.Model):
    class Meta:
        verbose_name = "Memória RAM"
        verbose_name_plural = "Memórias RAM"

    computador = models.ForeignKey(
        Computador, on_delete=models.CASCADE, related_name="memoria")
    memoria = models.ForeignKey(
        MemoriaRam, verbose_name="Memória RAM",
        on_delete=models.CASCADE, related_name="computador"
    )
