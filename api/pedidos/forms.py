from django import forms
from django.core.validators import ValidationError
from .models import Computador, ComputadorMemoria


class ComputadorMemoriaFormset(forms.BaseInlineFormSet):
    def clean(self, *args, **kwargs):
        if hasattr(self, "cleaned_data"):
            slots = 0
            memoria = 0
            for form in self.cleaned_data:
                if not form["DELETE"]:
                    slots += 1
                    memoria += form["memoria"].tamanho
            if slots > self.instance.placa_mae.slots_memoria:
                raise ValidationError("Excedio limite dos slots de memória da Placa Mãe.")
            if memoria > self.instance.placa_mae.memoria_suportaca:
                raise ValidationError("Excedio limite de memória da Placa Mãe.")
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
