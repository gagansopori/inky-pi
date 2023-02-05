import os
import textwrap

from inky import InkyWHAT
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont


class NewsBulletIn:
    def __init__(self):
        # self.inky_what = InkyWHAT("red")
        self.inky_what = auto()
        self.inky_what.set_border(self.inky_what.WHITE)

    def clear_screen(self):
        pass

    def build_font(self, text_h):
        return ImageFont.truetype('/home/pi/Oswald.ttf', int(text_h))

    def build_context(self, drawing_context):
        return ImageDraw.Draw(drawing_context)

    def measure_text(self, display_font, display_text, display_context):
        return display_context.textsize(display_text, font=display_font)

    def format_text(self, display_text, text_size):
        pass


    def draw_text(self):
        bg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT))
        font = self.build_font(bg.height/5)
        draw = self.build_context(bg)
        text = "Nikki Benz"
        x, y = bg.width/2, bg.height/2

        if len(text) < self.inky_what.WIDTH:
            print(len(text))

        for line in textwrap.wrap(text, width=(self.inky_what.WIDTH)):
            # print(line)
            w, h = font.getsize(line)
            # x += (self.inky_what.WIDTH / 2) - (w / 2)
            # y += (self.inky_what.HEIGHT / 2) - (h / 2)
            draw.text((x, y), line, self.inky_what.YELLOW, font)
            x += w
            y += h
            self.inky_what.set_image(bg)
            self.inky_what.show()
        return bg

    def draw_img(self):
        print(f'Inky Color: {self.inky_what.eeprom.get_color().title()}')
        
        img = Image.open("/home/pi/hanuman-art.jpeg")
        # img = img.rotate(90, expand=1)
        print(f'Original Image Size : {img.size}')

        rf = self.get_resize_factor(img)
        img_new = img.resize((int(img.width/rf),int(img.height/rf)), resample = Image.LANCZOS)
        img_new.save("/home/pi/test.png")
        img.close(), img_new.close()

        fg = Image.open("/home/pi/test.png")
        print(f'Foreground Image Size : {fg.size}')
        # bg = self.draw_text(fg, "Joanna Angel")
        bg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT))
        print(bg.size)

        # convert image to 3 palette from RGB
        pal_img = Image.new("P", (1,1))
        pal_img.putpalette((255,255,255,0,0,0,255,0,0) + (0,0,0)*252)
        fg = fg.convert("RGB").quantize(palette=pal_img)
        print(f'fg Size - {fg.size}')
        # position image in the center of the screen
        x,y = int((bg.width - fg.width)/2), int((bg.height - fg.height)/2)
        # x,y = 0,0
        Image.Image.paste(bg,fg, (x,y))
        print(bg.size)
        self.inky_what.set_image(bg)
        self.inky_what.show()


    def get_resize_factor(self, img):
        
        resize_factor = 1.0

        img_w, img_h = img.size
        rf_h, rf_w  = img_h/self.inky_what.HEIGHT, img_w/self.inky_what.WIDTH

        # if rf_w > rf_h:
        #     resize_factor = rf_w
        # else:
        #     resize_factor = rf_h
        # picture is taller than screen
        if img_h > self.inky_what.HEIGHT:
            print(f'picture is taller than screen')
            # picture is wider than screen
            if img_w > self.inky_what.WIDTH:
                print(f'picture is wider than screen')
                # picture mode (landscape)
                if rf_w > rf_h:
                    print(f'picture is wider than taller')
                    resize_factor = rf_w
                else:
                    resize_factor = rf_h
            else:
                print(f'picture is taller than wider')
                resize_factor = rf_h

        elif img_w > self.inky_what.WIDTH:
            resize_factor = rf_w

        print(f'Resize Factor: {resize_factor}')
        return resize_factor






if __name__ == '__main__':
    news = NewsBulletIn()
    # news.draw_text()
    news.draw_img()
