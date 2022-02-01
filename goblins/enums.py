from graphene import Enum


class ChatZone(Enum):
    """
    Define chat zones for messaging grouping.
    """
    GLOBAL = 'global'
    GROUP = 'group'
    GUILD = 'guild'
    DIRECT = 'direct'


class AvailableClasses(Enum):
    """
    Define as classes possiveis de serem criadas.
    """
    WARRIOR = 'warrior'
    RANGER = 'ranger'
    MAGICIAN = 'magician'


class AvailableMaps(Enum):
    FOREST = 'forest'
    PLAINS = 'plains'
    MOUNTAIN = 'mountain'
    SWAMP = 'swamp'
    RIVERSIDE = 'riverside'
    DESERT = 'desert'
    VILLAGE = 'village'
