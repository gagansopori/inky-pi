# from PIL import Image, ImageDraw, ImageFont
# from sources.inkypi import InitializeCustomLogger, DetectInkyBoard
# from sources.inkypi.ImageUtils import ImageProcessingUtil
#
#
# class BuildInkyImpressions:
#     def __init__(self):
#         # Setup Inky Board
#         self._inky = DetectInkyBoard()
#         self.imageutil = ImageProcessingUtil()
#         # Setup Logger
#         self.logger = InitializeCustomLogger(__class__.__name__)
#         # This value ranges from 0.1 - 1.0
#         self.color_saturation = 0.75
#
#     def image_driver(self, filepath) -> None:
#         self.logger.info(f'Beginning Image Preparation for Inky Impression Board.')
#         fg = self.imageutil.validate_image(filepath, (self._inky.inky.WIDTH, self._inky.inky.HEIGHT))
#
#         if fg:
#             foreground = self.prepare_canvas(fg)
#             background = self.prepare_canvas()
#             final_image = self.imageutil.prepare_image(foreground, background)
#
#             self._inky.inky.set_image(final_image, self.color_saturation)
#             self._inky.inky.show()
#
#     def prepare_canvas(self, mask=None) -> Image:
#         if mask:
#             self.logger.info("Creating Image Foreground")
#             mask = mask.convert("RGB")
#         else:
#             self.logger.info("Creating Image Background")
#             mask = Image.new("RGB", (self._inky.inky.WIDTH, self._inky.inky.HEIGHT), (255, 255, 255))
#
#         return mask
