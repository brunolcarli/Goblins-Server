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
        'luck': 5,
        'sprite': 'https://camo.githubusercontent.com/1375012e9b11f93ee428216fb47ae8e422ce9a11a3ac07f09f8af225bfe3cd6c/68747470733a2f2f692e6962622e636f2f353162376768722f676f626c696e2d72616e6765722e706e67'
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
        'luck': 2,
        'sprite': 'https://camo.githubusercontent.com/3739e2b658cf8dd84d44a2e42de6a9adb53a50c6cd6b3cd6b1c1d236cb54d55f/68747470733a2f2f692e6962622e636f2f4d32547a42487a2f676f626c696e2d77617272696f722e706e67'
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
        'luck': 2,
        'sprite': 'https://camo.githubusercontent.com/9fa6c2b363625395ca97a5d1287ff5fa024f2abb1162fd754dde4ab0cde7e5ea/68747470733a2f2f692e6962622e636f2f32674e676746712f676f626c696e2d6d6167696369616e2e706e67'
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
