import os
import textwrap

from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont


class NewsBulletIn:
    def __init__(self):
        self.inky_what = InkyWHAT("red")
        self.inky_what.set_border(self.inky_what.WHITE)


    def clear_screen(self):
        pass

    def build_font(self, text_h):
        if os.name == 'nt':
            return ImageFont.truetype('D:/zz2/Oswald.ttf', text_h)
        else:
            return ImageFont.truetype('%s/inky-pi/project/resources/Oswald.ttf' % (os.getcwd()), text_h)

    def build_context(self, drawing_context):
        return ImageDraw.Draw(drawing_context)

    def measure_text(self, display_font, display_text, display_context):
        return display_context.textsize(display_text, font=display_font)


    def draw_text(self):
        img = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT))
        font = self.build_font(self.inky_what.HEIGHT/5)
        draw = self.build_context(img)
        text = "Hello World! Can I get a WHAT WHAT?!"
        x, y = 0, 0
        for line in textwrap.wrap(text, width=self.inky_what.WIDTH):
            print(line)
            w, h = font.getsize(line)
            x += (self.inky_what.WIDTH / 2) - (w / 2)
            y += (self.inky_what.HEIGHT / 2) - (h / 2)
            draw.text((x, y), line, self.inky_what.RED, font)
            self.inky_what.set_image(img)
            self.inky_what.show()



if __name__ == '__main__':
    news = NewsBulletIn()
    news.draw_text()

