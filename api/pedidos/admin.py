from django.contrib import admin
from .models import Computador


class ComputadorAdmin(admin.ModelAdmin):
    filter_horizontal = ("memoria",)
admin.site.register(Computador, ComputadorAdmin)
