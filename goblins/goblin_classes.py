"""
Define as classes de personagem e seus atributos de base.
"""

class GoblinClasses:
    """
    Estrutura e definine as possíveis classes que podem ser escolhidas
    na criação de um personagem.
    """
    ranger = {
        'max_hp': 150,
        'max_mp': 50,
        'strength': 8,
        'defense': 7,
        'magic': 2,
        'spirit': 2,
        'max_range': 5,
        'movement': 2,
        'luck': 5
    }
    warrior = {
        'max_hp': 300,
        'max_mp': 50,
        'strength': 15,
        'defense': 12,
        'magic': 2,
        'spirit': 3,
        'max_range': 1,
        'movement': 1,
        'luck': 2
    }
    magician = {
        'max_hp': 120,
        'max_mp': 200,
        'strength': 2,
        'defense': 6,
        'magic': 15,
        'spirit': 14,
        'max_range': 1,
        'movement': 1,
        'luck': 2
    }

    @staticmethod
    def get_class(name):
        """
        Recupera os dados de uma das possíveis classes.
        """
        classes = {
            'ranger': GoblinClasses.ranger,
            'warrior': GoblinClasses.warrior,
            'magician': GoblinClasses.magician
        }
        return classes.get(name)
