from django.db import models

class Receita(models.Model):
    remedios = models.CharField(max_length=200) #separados por virgula
    medico = models.CharField(max_length = 200)
    data_criacao = models.DateTimeField(auto_now_add = True)
    observacoes = models.CharField(max_length=500, blank = True)