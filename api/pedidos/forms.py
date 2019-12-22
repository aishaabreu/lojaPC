from django import forms
from django.db.models import Sum
from django.core.validators import ValidationError
from .models import Computador, ComputadorMemoria


class ComputadorMemoriaFormset(forms.BaseInlineFormSet):
    def get_total_mem(self):
        """
            Calcula o total de slots e o total de memoria,
            levando em consideração adições, edições e remoções.
        """
        slots = self.instance.memoria.count()
        memoria = self.instance.memoria.aggregate(
            total=Sum('memoria__tamanho'))['total'] or 0

        if hasattr(self, "cleaned_data"):
            slots_adicionais = 0
            memoria_adicional = 0
            memorias_cadastradas = {
                mem.pk: mem.memoria.tamanho
                for mem in self.instance.memoria.all()
            }
            for form in self.cleaned_data:
                if form["DELETE"]:
                    memorias_cadastradas.pop(form["id"].pk, None)
                elif form["id"]:
                    memorias_cadastradas[form["id"].pk] = form["memoria"].tamanho
                else:
                    slots_adicionais += 1
                    memoria_adicional += form["memoria"].tamanho
            slots = len(memorias_cadastradas.keys()) + slots_adicionais
            memoria = sum(memorias_cadastradas.values()) + memoria_adicional

        return slots, memoria

    def clean(self, *args, **kwargs):
        """
            Validação das Memórias no Computador            
            verifica as regras de negócio:
                Deve haver sem uma memória RAM
                Não ultrapassar limite dos slots de memória da placa mãe
                Não ultrapassar limite de memória da placa mãe
        """

        slots, memoria = self.get_total_mem()

        if not slots:
            raise ValidationError("É obrigatório pelo menos uma Memória RAM.")
        if slots > self.instance.placa_mae.slots_memoria:
            raise ValidationError("Excedido limite dos slots de memória da Placa Mãe.")
        if memoria > self.instance.placa_mae.memoria_suportaca:
            raise ValidationError("Excedido limite de memória da Placa Mãe.")
        return super().clean(*args, **kwargs)


class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = "__all__"

    def clean(self, *args, **kwargs):
        processador = self.cleaned_data.get("processador", None)
        placa_mae = self.cleaned_data.get("placa_mae", None)
        placa_video = self.cleaned_data.get("placa_video", None)
        if processador and placa_mae and not placa_mae.processadores_suportados.filter(pk=processador.pk).exists():
            raise ValidationError("Placa Mãe não tem suporte para este processador.")
        if placa_mae and not placa_mae.video_integrado and not placa_video:
            raise ValidationError("Placa de Vídeo obrigatória para esta Placa Mãe.")
