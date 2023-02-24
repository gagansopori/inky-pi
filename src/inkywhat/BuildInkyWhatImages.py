from PIL import Image

from src import DetectInkyBoard, InitializeCustomLogger
from src.services.ImageUtils import ImageProcessingUtil


class BuildInkyWhatImages:
    def __init__(self):
        # Setup Inky Board
        self._inky = DetectInkyBoard()
        self.imageutil = ImageProcessingUtil()
        # Setup Logger
        self.logger = InitializeCustomLogger(__class__.__name__)
        # Get Inky Color
        self.color = self._inky.inky.eeprom.get_color()

    def image_driver(self, filepath) -> None:
        self.logger.info(f'Beginning Image Preparation for Inky WHat Board.')
        fg = self.imageutil.validate_image(filepath, (self._inky.inky.WIDTH, self._inky.inky.HEIGHT))
        if fg:
            foreground = self.prepare_canvas(fg)
            background = self.prepare_canvas()
            final_image = self.imageutil.prepare_image(foreground, background)

            self._inky.inky.set_image(final_image)
            self._inky.inky.show()

    def prepare_canvas(self, mask=None) -> Image:
        if mask:
            self.logger.info("Creating Image Foreground")
            mask = self.convert_color_palette(mask)
        else:
            self.logger.info("Creating Image Background")
            mask = Image.new("P", (self._inky.inky.WIDTH, self._inky.inky.HEIGHT))

        return mask

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
