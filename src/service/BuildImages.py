import os
from PIL import Image

class BuildInkyImages:
    def __init__(self):
        self.resize_factor: float = 1.0

    def prepare_image(self, filepath, filename, screen) -> Image:
        if not filename.endswith(".png"):
            og_img = Image.open(filepath + filename)
            new_img = self.resize_image(og_img, screen)
            self.save_to_disk(new_img, filepath, filename.split('.')[0])
            og_img.close(), new_img.close()

    def resize_image(self, image, display) -> Image:
        """
        Create a copy of the original image with refactors (Resizing, Resampling, etc...)
        :param display:
        :param image:
        :return:
        """
        rf = self.calculate_resize_factor(image, display)
        w, h = int(image.width / rf), int(image.height / rf)
        new_image = image.resize((w, h), resample=Image.LANCZOS)

        return new_image

    def calculate_resize_factor(self, image, display) -> float:
        """
        This method is common across all types of displays.
        :param display:
        :param image:
        :return:
        """
        disp_width, disp_height = display
        img_width, img_height = image.size
        rf_w, rf_h = img_width / disp_width, img_height / disp_height

        if img_height > disp_height:
            if img_width > disp_width:
                if rf_h > rf_w:
                    self.resize_factor = rf_h
                else:
                    self.resize_factor = rf_w
            else:
                self.resize_factor = rf_h
        elif img_width > disp_width:
            self.resize_factor = rf_w

        return self.resize_factor

    def save_to_disk(self, image, directory, filename):
        image.save(f'{directory}/{filename}.png')