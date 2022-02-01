from django.db import models
from django.contrib.auth import get_user_model

class Entity(models.Model):
    """
    Estrutura de dados armazenável que repesenta uma entidade.
    Uma entidade é qualquer elemento que possoa existir em um
    mundo possível.
    """
    reference = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    location = models.BinaryField()
    logged = models.BooleanField(null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)


class Character(models.Model):
    """
    Estrutura de dados para representar os atributos de um personagem.
    Um personagem é uma entidade jogável com características individuais.
    """
    name = models.CharField(max_length=50)
    current_hp = models.IntegerField(default=200)
    current_mp = models.IntegerField(default=100)
    max_hp = models.IntegerField(default=200)
    max_mp = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    defense = models.IntegerField(default=10)
    magic = models.IntegerField(default=10)
    spirit = models.IntegerField(default=10)
    experience = models.IntegerField(default=0)
    next_lv = models.IntegerField(default=1)
    lv = models.IntegerField(default=1)
    max_range = models.IntegerField(default=1)
    movement = models.IntegerField(default=1)
    luck = models.IntegerField(default=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField('goblins.Skill')
    goblin_class = models.CharField(max_length=25, null=True)


class Skill(models.Model):
    """
    Estrutura de dados para representar uma habilidade.
    Habilidade é uma caracteristica aprendivel e utilizavel por um personagem.
    """
    name = models.CharField(max_length=50)
    power = models.IntegerField()
    additional_range = models.IntegerField(default=0)
    area_of_effect = models.IntegerField(default=1)
    effect_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
