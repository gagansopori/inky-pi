import os, textwrap

from inky.auto import auto
from PIL import Image,ImageDraw,ImageFont


class BuildInkyImages:
    def __init__(self):
        self.inky_what = auto()
        self.inky_what.set_border(self.inky_what.WHITE)

        self.color = self.inky_what.eeprom.get_color()
        self.resize_factor: float = 1.0

    def prepare_image(self, filepath, filename) -> Image:
        if not filename.endswith(".png"):
            og_img = Image.open(filepath + filename)
            new_img = self.resize_image(og_img)
            self.save_to_disk(new_img, filepath, filename.split('.')[0])
            og_img.close()
        else:
            fg = Image.open(filepath + filename)
            fg_new = self.convert_color_palette(fg)
            bg = Image.new("P",(self.inky_what.WIDTH, self.inky_what.HEIGHT))
            # x,y -> coordinates to place fg on bg. Top Left = (0,0)
            x,y = int((bg.width - fg.width)/2), int((bg.height - fg.height)/2)
            Image.Image.paste(bg,fg_new, (x,y))
        return bg

    def resize_image(self, image) -> Image:
        rf = self.calculate_resize_factor(image)
        w,h = int(image.width/rf), int(image.height/rf)
        new_image = image.resize((w,h), resample=Image.LANCZOS)
        return new_image

    def calculate_resize_factor(self, image) -> float:
        """
        This method is common across all types of displays.
        :param image:
        :return:
        """
        img_width, img_height = image.size
        rf_w, rf_h = img_width/self.inky_what.HEIGHT, img_height/self.inky_what.WIDTH

        if rf_h > rf_w:
            self.resize_factor = rf_h
        else:
            self.resize_factor = rf_w

        # if img_height > self.inky_what.HEIGHT:
        #     if img_width > self.inky_what.WIDTH:
        #         if img_width > img_height:
        #             self.resize_factor = img_width/self.inky_what.WIDTH
        #         else:
        #             self.resize_factor = img_height/self.inky_what.HEIGHT
        #     else:
        #         self.resize_factor = img_height/self.inky_what.HEIGHT
        # elif img_width > self.inky_what.WIDTH:
        #     self.resize_factor = img_width/self.inky_what.WIDTH

        return self.resize_factor

    def convert_color_palette(self, image) -> Image:
        """
        Utility method that takes in an Image Object and converts the palette from RGB to 3 color for InkyWHAT or ePaper
        Displays
        :param image:
        :return:
        """
        pal_img = Image.new("P", (1,1))
        # Need to check if RGB values work differently with each variant or the board.
        pal_img.putpalette((255,255,255,0,0,0,255,0,0) + (0,0,0)*252)
        image = image.convert("RGB").quantize(palette=pal_img)

        return image

    def save_to_disk(self, image, directory, filename):
        image.save(f'{directory}/{filename}.png')
        pass


