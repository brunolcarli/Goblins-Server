

class MapSizes:
    """
    Define tamanhos máximos para os cenários.
    """
    forest = (528, 624)
    plains = (720, 720)
    mountain = (480, 720)
    swamp = (336, 240)
    riverside = (240, 528)
    desert = (816, 816)
    village = (336, 336)

    @staticmethod
    def get_map_size(name):
        maps = {
            'forest': MapSizes.forest,
            'plains': MapSizes.plains,
            'mountain': MapSizes.mountain,
            'swamp': MapSizes.swamp,
            'riverside': MapSizes.riverside,
            'desert': MapSizes.desert,
            'village': MapSizes.village
        }
        return maps.get(name)
