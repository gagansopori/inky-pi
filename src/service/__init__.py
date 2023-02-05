from inky.auto import auto

class InitializeInkyDisplay:
    def __init__(self):
        self.inky_display = auto(verbose=True)
        self.inky_display.set_border(self.inky_display.WHITE)