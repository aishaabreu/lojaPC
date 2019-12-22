from django.db import models
from django.conf import settings
from produtos.models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo


class Computador(models.Model):
    class Meta:
        verbose_name_plural = "Computadores"

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    processador = models.ForeignKey(Processador, on_delete=models.PROTECT)
    placa_mae = models.ForeignKey(
        PlacaMae, verbose_name="Placa Mãe", on_delete=models.PROTECT)
    memoria = models.ManyToManyField(
        MemoriaRam, verbose_name="Memória RAM")
    placa_video = models.ForeignKey(
        PlacaDeVideo, verbose_name="Placa de Vídeo",
        null=True, blank=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return "{cliente} - {processador}({placa_mae})".format(
            cliente=self.cliente.first_name,
            processador=self.processador,
            placa_mae=self.placa_mae,
        )