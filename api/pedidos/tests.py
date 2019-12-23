import json
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework import status
from produtos.models import Processador, PlacaMae, MemoriaRam, PlacaDeVideo
from .models import Computador
from .forms import (ERRO_MEMORIA_OBRIGATORIA,
    ERRO_SLOTS_MEMORIA,
    ERRO_LIMITE_MEMORIA,
    ERRO_PLACA_MAE_INCOMPATIVEL,
    ERRO_PLACA_VIDEO_OBRIGATORIA,)


class PedidoAdminTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            "super_user", password="12#45678"
        )
        self.client.force_login(self.user)
        self.processador_intel = Processador.objects.create(
            descricao="Processador Intel Core i7",
            marca=Processador.INTEL
        )
        self.processador_amd = Processador.objects.create(
            descricao="Processador AMD Ryzen 7",
            marca=Processador.AMD
        )
        self.placa_mae_suporte_intel = PlacaMae.objects.create(
            descricao="Placa Mãe suporte Intel",
            slots_memoria=2,
            memoria_suportaca=32,
            video_integrado=False
        )
        self.placa_mae_suporte_intel.processadores_suportados.add(
            self.processador_intel
        )
        self.memoria_4gb = MemoriaRam.objects.create(
            descricao="Memória RAM de Teste",
            tamanho=4,
        )
        self.memoria_64gb = MemoriaRam.objects.create(
            descricao="Memória RAM de Teste",
            tamanho=64,
        )
        self.placa_video = PlacaDeVideo.objects.create(
            descricao="Placa de Vídeo de Teste",
        )

    def create_memoria_inline_data(self, memorias):
        inline_data = {
            "memoria-TOTAL_FORMS":len(memorias),
            "memoria-INITIAL_FORMS": 0,
            "memoria-MIN_NUM_FORMS": 1,
            "memoria-MAX_NUM_FORMS": 1000
        }

        for index, mem in enumerate(memorias):
            inline_data.update({
                "memoria-{index}-id".format(index=index): "",
                "memoria-{index}-computador".format(index=index): "",
                "memoria-{index}-memoria".format(index=index): mem
            })

        return inline_data

    def test_posso_montar_um_computador(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_intel.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": self.placa_video.pk
        }

        memoria = [self.memoria_4gb.pk]
        data.update(self.create_memoria_inline_data(memoria))

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        computador = Computador.objects.get()
        self.assertEqual(computador.cliente.pk, data["cliente"])
        self.assertEqual(computador.processador.pk, data["processador"])
        self.assertEqual(computador.placa_mae.pk, data["placa_mae"])
        self.assertEqual(
            list(computador.memoria.values_list("memoria__pk", flat=True)),
            memoria
        )
        self.assertEqual(computador.placa_video.pk, data["placa_video"])

    def test_nao_posso_escolher_uma_placa_nao_suportada(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_amd.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": self.placa_video.pk
        }

        data.update(self.create_memoria_inline_data([self.memoria_4gb.pk]))

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        self.assertFalse(Computador.objects.exists())
        self.assertContains(response, ERRO_PLACA_MAE_INCOMPATIVEL)

    def test_nao_posso_montar_computador_sem_memoria_ram(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_intel.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": self.placa_video.pk,
            "memoria-TOTAL_FORMS": 0,
            "memoria-INITIAL_FORMS": 0,
            "memoria-MIN_NUM_FORMS": 1,
            "memoria-MAX_NUM_FORMS": 1000
        }

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        self.assertFalse(Computador.objects.exists())
        self.assertContains(response, ERRO_MEMORIA_OBRIGATORIA)

    def test_posso_adicionar_varias_memorias_do_mesmo_tamanho(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_intel.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": self.placa_video.pk
        }

        memoria = [self.memoria_4gb.pk, self.memoria_4gb.pk]
        data.update(self.create_memoria_inline_data(memoria))

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        computador = Computador.objects.get()
        self.assertEqual(computador.cliente.pk, data["cliente"])
        self.assertEqual(computador.processador.pk, data["processador"])
        self.assertEqual(computador.placa_mae.pk, data["placa_mae"])
        self.assertEqual(
            list(computador.memoria.values_list("memoria__pk", flat=True)),
            memoria
        )
        self.assertEqual(computador.placa_video.pk, data["placa_video"])

    def test_nao_posso_exceder_os_slots_de_memoria(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_intel.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": self.placa_video.pk,
        }

        memoria = [
            self.memoria_4gb.pk,
            self.memoria_4gb.pk,
            self.memoria_4gb.pk,
            self.memoria_4gb.pk,
        ]
        data.update(self.create_memoria_inline_data(memoria))

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        self.assertFalse(Computador.objects.exists())
        self.assertContains(response, ERRO_SLOTS_MEMORIA)

    def test_nao_posso_exceder_a_memoria_suportada(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_intel.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": self.placa_video.pk,
        }

        memoria = [
            self.memoria_64gb.pk,
        ]
        data.update(self.create_memoria_inline_data(memoria))

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        self.assertFalse(Computador.objects.exists())
        self.assertContains(response, ERRO_LIMITE_MEMORIA)

    def test_placa_de_video_obrigatorio_quando_nao_possui_video_integrado(self):
        data = {
            "cliente": self.user.pk,
            "processador": self.processador_intel.pk,
            "placa_mae": self.placa_mae_suporte_intel.pk,
            "placa_video": "",
        }

        memoria = [
            self.memoria_4gb.pk,
            self.memoria_4gb.pk,
        ]

        data.update(self.create_memoria_inline_data(memoria))

        response = self.client.post(
            reverse_lazy("admin:pedidos_computador_add"), data)

        self.assertFalse(Computador.objects.exists())
        self.assertContains(response, ERRO_PLACA_VIDEO_OBRIGATORIA)


class PedidoAPITest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            "super_user", password="12#45678"
        )
        self.client.force_login(self.user)
        self.processador_intel = Processador.objects.create(
            descricao="Processador Intel Core i7",
            marca=Processador.INTEL
        )
        self.processador_amd = Processador.objects.create(
            descricao="Processador AMD Ryzen 7",
            marca=Processador.AMD
        )
        self.placa_mae_suporte_intel = PlacaMae.objects.create(
            descricao="Placa Mãe suporte Intel",
            slots_memoria=2,
            memoria_suportaca=32,
            video_integrado=False
        )
        self.placa_mae_suporte_intel.processadores_suportados.add(
            self.processador_intel
        )
        self.memoria_4gb = MemoriaRam.objects.create(
            descricao="Memória RAM de Teste",
            tamanho=4,
        )
        self.memoria_64gb = MemoriaRam.objects.create(
            descricao="Memória RAM de Teste",
            tamanho=64,
        )
        self.placa_video = PlacaDeVideo.objects.create(
            descricao="Placa de Vídeo de Teste",
        )

    def reverse(self, name, *args):
        return "http://testserver{path}".format(
            path=reverse_lazy(name, args=args))

    def test_posso_montar_um_computador(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_intel.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": self.reverse(
                "placadevideo-detail", self.placa_video.pk),
            "memoria": [{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            }]
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        computador = Computador.objects.get()
        self.assertEqual(computador.cliente.pk, self.user.pk)
        self.assertEqual(computador.processador.pk, self.processador_intel.pk)
        self.assertEqual(computador.placa_mae.pk, self.placa_mae_suporte_intel.pk)
        self.assertEqual(computador.placa_video.pk, self.placa_video.pk)
        self.assertEqual(
            list(computador.memoria.values_list("memoria__pk", flat=True)),
            [self.memoria_4gb.pk]
        )

    def test_nao_posso_escolher_uma_placa_nao_suportada(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_amd.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": self.reverse(
                "placadevideo-detail", self.placa_video.pk),
            "memoria": [{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            }]
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertFalse(Computador.objects.exists())
        self.assertContains(
            response, ERRO_PLACA_MAE_INCOMPATIVEL,
            status_code=status.HTTP_400_BAD_REQUEST)

    def test_nao_posso_montar_computador_sem_memoria_ram(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_intel.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": self.reverse(
                "placadevideo-detail", self.placa_video.pk),
            "memoria": []
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertFalse(Computador.objects.exists())
        self.assertContains(
            response, ERRO_MEMORIA_OBRIGATORIA,
            status_code=status.HTTP_400_BAD_REQUEST)

    def test_posso_adicionar_varias_memorias_do_mesmo_tamanho(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_intel.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": self.reverse(
                "placadevideo-detail", self.placa_video.pk),
            "memoria": [{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            },{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            }]
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        computador = Computador.objects.get()
        self.assertEqual(computador.cliente.pk, self.user.pk)
        self.assertEqual(computador.processador.pk, self.processador_intel.pk)
        self.assertEqual(computador.placa_mae.pk, self.placa_mae_suporte_intel.pk)
        self.assertEqual(computador.placa_video.pk, self.placa_video.pk)
        self.assertEqual(
            list(computador.memoria.values_list("memoria__pk", flat=True)),
            [self.memoria_4gb.pk, self.memoria_4gb.pk]
        )

    def test_nao_posso_exceder_os_slots_de_memoria(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_intel.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": self.reverse(
                "placadevideo-detail", self.placa_video.pk),
            "memoria": [{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            },{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            },{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            }]
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertFalse(Computador.objects.exists())
        self.assertContains(
            response, ERRO_SLOTS_MEMORIA,
            status_code=status.HTTP_400_BAD_REQUEST)

    def test_nao_posso_exceder_a_memoria_suportada(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_intel.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": self.reverse(
                "placadevideo-detail", self.placa_video.pk),
            "memoria": [{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_64gb.pk)
            }]
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertFalse(Computador.objects.exists())
        self.assertContains(
            response, ERRO_LIMITE_MEMORIA,
            status_code=status.HTTP_400_BAD_REQUEST)

    def test_placa_de_video_obrigatorio_quando_nao_possui_video_integrado(self):
        data = {
            "cliente": self.reverse("user-detail", self.user.pk),
            "processador": self.reverse(
                "processador-detail", self.processador_intel.pk),
            "placa_mae": self.reverse(
                "placamae-detail", self.placa_mae_suporte_intel.pk),
            "placa_video": "",
            "memoria": [{
                "memoria": self.reverse(
                    "memoriaram-detail", self.memoria_4gb.pk)
            }]
        }

        response = self.client.post(
            reverse_lazy("computador-list"),
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertFalse(Computador.objects.exists())
        self.assertContains(
            response, ERRO_PLACA_VIDEO_OBRIGATORIA,
            status_code=status.HTTP_400_BAD_REQUEST)
