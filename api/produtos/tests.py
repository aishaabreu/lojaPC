from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo


class ProdutosAdminTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            "super_user", password="12#45678"
        )
        self.client.force_login(self.user)

    def test_posso_cadastrar_um_processador(self):
        data = {
            "descricao": "Processador de Teste",
            "marca": Processador.AMD
        }

        response = self.client.post(
            reverse_lazy("admin:produtos_processador_add"), data)
        
        processador = Processador.objects.get()
        self.assertEqual(processador.descricao, data["descricao"])
        self.assertEqual(processador.marca, data["marca"])

    def test_posso_cadastrar_uma_placa_mae(self):
        processador = Processador.objects.create(
            descricao="Processador de Teste",
            marca=Processador.AMD
        )

        data = {
            "descricao": "Placa Mãe de Teste",
            "processadores_suportados": [processador.pk],
            "slots_memoria": 2,
            "memoria_suportaca": 32,
            "video_integrado": False
        }

        response = self.client.post(
            reverse_lazy("admin:produtos_placamae_add"), data)

        placa = PlacaMae.objects.get()
        self.assertEqual(placa.descricao, data["descricao"])
        self.assertEqual(
            list(placa.processadores_suportados.values_list("pk", flat=True)),
            data["processadores_suportados"]
        )
        self.assertEqual(placa.slots_memoria, data["slots_memoria"])
        self.assertEqual(placa.memoria_suportaca, data["memoria_suportaca"])
        self.assertEqual(placa.video_integrado, data["video_integrado"])

    def test_posso_cadastrar_uma_memoria_ram(self):
        data = {
            "descricao": "Memória de Teste",
            "tamanho": 8
        }

        response = self.client.post(
            reverse_lazy("admin:produtos_memoriaram_add"), data)
        
        memoria = MemoriaRam.objects.get()
        self.assertEqual(memoria.descricao, data["descricao"])
        self.assertEqual(memoria.tamanho, data["tamanho"])

    def test_posso_cadastrar_uma_placa_de_video(self):
        data = {
            "descricao": "Placa de Vídeo de Teste",
        }

        response = self.client.post(
            reverse_lazy("admin:produtos_placadevideo_add"), data)
        
        placa = PlacaDeVideo.objects.get()
        self.assertEqual(placa.descricao, data["descricao"])
