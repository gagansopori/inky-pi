
from inky.auto import auto


class BuildInkyImages:
    def __init__(self):
        self._inky = auto()
        self._inky.set_border(self._inky.WHITE)

        # This value ranges from 0.1 - 1.0
        self.image_saturation = 0.5

