from django.contrib import admin
from .models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo


admin.site.register(Processador)
admin.site.register(MemoriaRam)
admin.site.register(PlacaDeVideo)


class PlacaMaeAdmin(admin.ModelAdmin):
    filter_horizontal = ("processadores_suportados",)
admin.site.register(PlacaMae, PlacaMaeAdmin)
