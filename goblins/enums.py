import graphene


class ChatZone(graphene.Enum):
    """
    Define chat zones for messaging grouping.
    """
    GLOBAL = 'global'
    GROUP = 'group'
    GUILD = 'guild'
    DIRECT = 'direct'
