# import PIL
# from PIL import Image
#
# from sources.inkypi import InitializeCustomLogger
#
#
# class ImageProcessingUtil:
#     def __init__(self):
#         # Setup Logger
#         self.logger = InitializeCustomLogger(__class__.__name__)
#         # Default Resize Factor for images
#         self.resize_factor: float = 1.0
#
#     def validate_image(self, filepath, epaper_dimensions) -> Image:
#         """
#         This method validates whether the directory & filename arguments point to a valid image in .png format. This
#         method is not supposed to raise an exception, as there maybe multiple image files provided via a directory & the
#         possibility of a corrupted image is not NIL.
#         :param epaper_dimensions:
#         :param filepath:
#         :return:
#         """
#         self.logger.info(f'Beginning Image Validation Procedure.')
#         try:
#             with Image.open(filepath) as og_img:
#                 self.logger.info(f'Successfully opened & recognized Image. Checking for other modifications.')
#                 # Validate if the picture is in portrait or landscape mode & control Servo To Rotate Frame
#                 # Get Exif Tags - GPS Info, if there is any.
#                 new_img = self.resize_image(og_img, epaper_dimensions)
#                 return new_img
#         except FileNotFoundError as fnf:
#             self.logger.error(f'{fnf}\nInvalid filepath provided for image: {filepath}.')
#             return None
#         except PIL.UnidentifiedImageError as uimg:
#             self.logger.error(f'{uimg}\nCannot identify image: {filepath}.')
#             return None
#         except (TypeError, ValueError) as tv:
#             self.logger.error(f'{tv}')
#             return None
#
#     def resize_image(self, image, epaper_dimensions) -> Image:
#         """
#         Create a copy of the original image with refactors (Resizing, Resampling, etc...)
#         :param epaper_dimensions:
#         :param image:
#         :return:
#         """
#         self.logger.info(f'Beginning Image Resizing Procedure.')
#         rf = self.calculate_resize_factor(image, epaper_dimensions)
#         self.logger.info(f'Calculated Resize Factor: {rf}.')
#         w, h = int(image.width / rf), int(image.height / rf)
#         new_image = image.resize((w, h), resample=Image.LANCZOS)
#
#         return new_image
#
#     def calculate_resize_factor(self, image, epd_size) -> float:
#         """
#         This method is common across all types of displays.
#         :param epd_size:
#         :param image:
#         :return:
#         """
#         disp_width, disp_height = epd_size
#         img_width, img_height = image.size
#         rf_w, rf_h = img_width / disp_width, img_height / disp_height
#
#         if img_height > disp_height:
#             if img_width > disp_width:
#                 if rf_h > rf_w:
#                     self.logger.info(f'Image is in Portrait Mode. Resizing Accordingly.')
#                     self.resize_factor = rf_h
#                 else:
#                     self.logger.info(f'Image is in Landscape Mode. Resizing Accordingly.')
#                     self.resize_factor = rf_w
#             else:
#                 self.logger.info(f'Portrait Mode Image with Lower than Screen-Width. Resizing Accordingly.')
#                 self.resize_factor = rf_h
#         elif img_width > disp_width:
#             self.logger.info(f'Landscape Mode Image with Lower than Screen-Height. Resizing Accordingly.')
#             self.resize_factor = rf_w
#
#         return self.resize_factor
#
#     def prepare_image(self, fg, bg):
#         # x,y -> coordinates to place fg on bg. Top Left = (0,0)
#         x, y = int((bg.width - fg.width) / 2), int((bg.height - fg.height) / 2)
#         Image.Image.paste(bg, fg, (x, y))
#         return bg
