from django.db import models


class Produto(models.Model):
    class Meta:
        abstract = True

    descricao = models.CharField(
        verbose_name="Descrição do Produto", max_length=50
    )

    def __str__(self):
        return self.descricao


class Processador(Produto):
    AMD = "amd"
    INTEL = "intel"

    OPCOES_MARCAS = (
        (AMD, "AMD"),
        (INTEL, "Intel")
    )

    class Meta:
        verbose_name_plural = "Processadores"

    marca = models.CharField(choices=OPCOES_MARCAS, max_length=5)


class PlacaMae(Produto):
    class Meta:
        verbose_name = "Placa Mãe"
        verbose_name_plural = "Placas Mãe"

    processadores_suportados = models.ManyToManyField(
        Processador, related_name="placas_com_suporte")
    slots_memoria = models.PositiveSmallIntegerField(
        verbose_name="Qtde. slots de memória RAM"
    )
    memoria_suportaca = models.PositiveSmallIntegerField(
        verbose_name="Total de memória RAM suportado"
    )
    video_integrado = models.BooleanField(
        verbose_name="Vídeo Integrado"
    )


class MemoriaRam(Produto):
    OPCOES_TAMANHOS = (
        (4, "4 GB"),
        (8, "8 GB"),
        (16, "16 GB"),
        (32, "32 GB"),
        (64, "64 GB")
    )

    class Meta:
        verbose_name = "Memória RAM"
        verbose_name_plural = "Memórias RAM"

    tamanho = models.PositiveSmallIntegerField(
        choices=OPCOES_TAMANHOS
    )

    def __str__(self):
        return "{descricao} {tamanho} GB".format(
            self.descricao, self.tamanho)


class PlacaDeVideo(Produto):
    class Meta:
        verbose_name = "Placa de Vídeo"
        verbose_name_plural = "Placas de Vídeo"
