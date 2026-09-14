from django.db import models

# Create your models here.

class Pessoa (models.Model):

    nome = models.CharField(max_length = 150)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length = 14)
    telefone = models.CharField(max_length = 20)
    nome_responsavel = models.CharField(max_length = 150, blank = True)
    estado_civil = models.CharField(max_length = 30)
    endereco = models.CharField(max_length = 260, blank = True)
    data_entrada = models.DateField()
    origen_cadastro = models.CharField(max_length = 20)

