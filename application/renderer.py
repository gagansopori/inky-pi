from PIL import Image, ImageDraw
from inky.auto import auto


class InkyRenderer:
    def __init__(self):
        try:
            self.display = auto()
        except:
            self.display = None

    def draw(self, widgets, mode):
        img = Image.new("P", (400, 300), color=0)
        draw = ImageDraw.Draw(img)

        if mode == 'grid':
            coords = [(0, 0, 400, 150), (0, 150, 200, 150), (200, 150, 200, 150)]
            for i, w in enumerate(widgets):
                x, y, width, height = coords[i]
                w.draw(draw, x, y, width, height)
                draw.rectangle([x, y, x + width, y + height], outline=1)
        else:
            widgets[0].draw(draw, 0, 0, 400, 300)

        if self.display:
            self.display.set_image(img)
            self.display.show()