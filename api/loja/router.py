from rest_framework import routers
from produtos import views as produtos_views
from pedidos import views as pedidos_views


router = routers.DefaultRouter()
router.register(r'processadores', produtos_views.ProcessadorViewSet)
router.register(r'placas-maes', produtos_views.PlacaMaeViewSet)
router.register(r'memorias-ram', produtos_views.MemoriaRamViewSet)
router.register(r'placas-de-video', produtos_views.PlacaDeVideoViewSet)
router.register(r'computador', pedidos_views.ComputadorViewSet)
router.register(r'usuario', pedidos_views.UserViewSet)