from django.contrib import admin
from .models import Computador, ComputadorMemoria
from .forms import ComputadorForm, ComputadorMemoriaFormset


class ComputadorMemoriaInline(admin.TabularInline):
    formset = ComputadorMemoriaFormset
    model = ComputadorMemoria
    min_num = 1
    extra = 0


class ComputadorAdmin(admin.ModelAdmin):
    form = ComputadorForm
    inlines = (ComputadorMemoriaInline,)
admin.site.register(Computador, ComputadorAdmin)
