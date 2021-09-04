from django.db import models


class Entity(models.Model):
    """
    Estrutura de dados armazenável que repesenta uma entidade.
    Uma entidade é qualquer elemento que possoa existir em um
    mundo possível.
    """
    reference = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    location = models.BinaryField()
    logged = models.BooleanField()
