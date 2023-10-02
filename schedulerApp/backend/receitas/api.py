from receitas.models import Receita
from rest_framework import viewsets, permissions
from .serializers import ReceitaSerializer

class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ReceitaSerializer