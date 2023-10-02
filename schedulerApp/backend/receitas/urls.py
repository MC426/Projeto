from rest_framework import routers
from .api import ReceitaViewSet

router = routers.DefaultRouter()
router.register('api/receitas', ReceitaViewSet, 'receita')

urlpatterns = router.urls