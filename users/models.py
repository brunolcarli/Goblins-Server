from django.db import models


# Create your models here.
class TokenBlackList(models.Model):
    '''
    Define tokens bloqueados no sistema.
    Tokens listados aqui não poderão ser autenticados.
    '''
    token = models.TextField()
