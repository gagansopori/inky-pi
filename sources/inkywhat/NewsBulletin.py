# import os,math
# import textwrap, feedparser
#
# from inky.auto import auto
# from PIL import Image, ImageDraw, ImageFont
#
#
# class NewsBulletIn:
#     def __init__(self):
#         # self.inky_what = InkyWHAT("red")
#         self.inky_what = auto()
#         self.inky_what.set_border(self.inky_what.WHITE)
#         self.news_url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
#         print(self.inky_what.eeprom.get_variant())
#         print(self.inky_what.eeprom.display_variant)
#
#     def clear_screen(self):
#         pass
#
#     def build_font(self, text_h):
#         return ImageFont.truetype('/home/pi/Oswald.ttf', int(text_h))
#
#     def build_context(self, drawing_context):
#         return ImageDraw.Draw(drawing_context)
#
#     def measure_text(self, display_font, display_text, display_context):
#         return display_context.textsize(display_text, font=display_font)
#
#     def setup_widget(self):
#         w, h = int(self.inky_what.WIDTH/2), int(self.inky_what.HEIGHT/2)
#         x, y = 0,0
#
#         # fg = Image.new("P", (w, h))
#         fg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT), self.inky_what.BLACK)
#         print(fg.size)
#         img_new = ImageDraw.Draw(fg)
#         img_new.rectangle([(0,0), (w-1,h-1)], fill = self.inky_what.RED, outline = self.inky_what.BLACK)
#
#         img_new.rectangle([(0,h), ((w*2)-1,(2*h)-1)], outline = self.inky_what.BLACK)
#
#         # fg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT),0)
#
#         # Image.Image.paste(fg,fg_1, (x,y))
#         # Image.Image.paste(fg_2,fg, (x, y))
#
#         # bg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT),0)
#
#         # Image.Image.paste(bg,fg, (x,y))
#
#
#
#         # self.inky_what.set_image(fg)
#         # self.inky_what.show()
#         return fg
#
#
#
#
#     def draw_text(self, bg):
#         # news = feedparser.parse(self.news_url)
#         # headline = news.entries[7].title
#         # headline = "कर्पूरगौरं करुणावतारं संसारसारम् भुजगेन्द्रहारम् । सदावसन्तं हृदयारविन्दे भवं भवानीसहितं नमामि ॥"
#         # detail = news.entries[0].description
#         # print(news.entries)
#
#         # bg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT),0)
#         # bg = self.setup_widget()
#
#         if not self.inky_what.eeprom.display_variant in (10,11,12,16):
#             heading = self.build_font(bg.height/12)
#             body = self.build_font(bg.height/16)
#         else:
#             heading = self.build_font(16)
#             body = self.build_font(12)
#
#         kntxt = self.build_context(bg)
#         x, y = 0,int(self.inky_what.HEIGHT/2)+5 # Padding
#
#         # print(f'TextSize = {self.measure_text(heading, headline, kntxt)}')
#         # print(f'Divide Ratio = {self.measure_text(font, text, draw)[0]/(self.inky_what.WIDTH)}')
#         # if len(text) < self.inky_what.WIDTH:
#         #     print(len(text))
#         #     print(text)
#
#         sentence = "Florida, US" #headline.split()
#         # sentence2 = detail.split()
#         hl, h2= "", ""
#         ll,l2 =0,0
#         final_list = []
#         body_list = []
#
#         for words in sentence:
#             word = words + " "
#             w,h = heading.getsize(word)
#
#             ll += w
#             if ll <= self.inky_what.WIDTH:
#                 hl += word
#             elif ll - heading.getsize(" ")[0] <= self.inky_what.WIDTH:
#                 hl += word
#             else:
#                 ll = w
#                 final_list.append(hl)
#                 hl=word
#             # print(hl)
#         final_list.append(hl)
#         print(final_list)
#
#
#         for line in final_list:
#             # print(line)
#             w,h = heading.getsize(line)
#             print(f'Font.GetSize = {heading.getlength(line)}')
#             x = (self.inky_what.WIDTH / 2) - (w/2)
#             # x = 0
#             # print(f'x={x}, y={y}')
#             kntxt.text((x, y), line, self.inky_what.WHITE, heading)
#             y += h
#
#
#         # for words in sentence2:
#         #     word = words + " "
#         #     w,h = body.getsize(word)
#
#         #     l2 += w
#         #     if l2 < self.inky_what.WIDTH:
#         #         h2 += word
#         #     else:
#         #         l2 = w
#         #         body_list.append(h2)
#         #         h2=word
#         #     # print(hl)
#         # body_list.append(h2)
#         # print(body_list)
#
#         # x, y = 0, y+10
#         # for line in body_list:
#         #     # print(line)
#         #     w,h = body.getsize(line)
#         #     # print(f'Font.GetSize = {body.getsize(line)}')
#         #     # x = 0
#         #     x = ((self.inky_what.WIDTH / 2) - (w / 2))
#         #     # print(f'x={x}, y={y}')
#         #     kntxt.text((x, y), line, self.inky_what.BLACK, body)
#         #     y += h
#
#         # for line in textwrap.wrap(headline, width=(self.inky_what.WIDTH)/10):
#         #     print(line)
#         #     w, h = heading.getsize(line)
#         #     # print(f'Font.GetSize = {font.getsize(line)}')
#         #     x = (self.inky_what.WIDTH / 2) - (w / 2)
#         #     # y += (self.inky_what.HEIGHT / 2) - (h / 2)
#         #     print(f'x={x}, y={y}')
#         #     kntxt.text((x, y), line, self.inky_what.RED, heading)
#         #     y += h
#         print(f'BG Size - {bg.size}')
#         # self.inky_what.set_image(bg)
#         # self.inky_what.show()
#         return bg
#
#     def draw_img(self):
#         print(f'Inky Color: {self.inky_what.eeprom.get_color()}')
#         print(f'Inky Dimensions: ({self.inky_what.WIDTH} x {self.inky_what.HEIGHT})')
#
#         img = Image.open("/home/pi/IMG_6183.JPEG")
#         img = img.rotate(90, expand=1)
#         print(f'Original Image Size : {img.size}')
#
#         rf = self.get_resize_factor(img)
#         img_new = img.resize((int(img.width/rf),int(img.height/rf)), resample = Image.LANCZOS)
#         img_new.save("/home/pi/test.png")
#         img.close(), img_new.close()
#
#         fg = Image.open("/home/pi/test.png")
#         print(f'Foreground Image Size : {fg.size}')
#         fg = self.draw_text(fg)
#         bg = Image.new("P", (self.inky_what.WIDTH, self.inky_what.HEIGHT), (255,255,255))
#         print(bg.size)
#
#         # convert image to 3 palette from RGB
#         pal_img = Image.new("P", (1,1))
#         pal_img.putpalette((255,255,255,0,0,0,255,0,0) + (0,0,0)*252)
#         fg = fg.convert("RGB").quantize(palette=pal_img)
#         print(f'fg Size - {fg.size}')
#         # position image in the center of the screen
#         # x,y = int((bg.width - fg.width)/2), int((bg.height - fg.height)/2)
#         x,y = fg.width,int((bg.height - fg.height)/2)
#         Image.Image.paste(bg,fg, (x,y))
#         print(bg.size)
#         # Image.Image.paste(bg, ImageDraw.Draw(mg), (1,1))
#         self.inky_what.set_image(bg)
#         self.inky_what.show()
#
#
#     def get_resize_factor(self, img):
#
#         resize_factor = 1.0
#
#         img_w, img_h = img.size
#         rf_h, rf_w  = img_h/self.inky_what.HEIGHT, img_w/self.inky_what.WIDTH
#
#         # if rf_w > rf_h:
#         #     resize_factor = rf_w
#         # else:
#         #     resize_factor = rf_h
#         # picture is taller than screen
#         if img_h > self.inky_what.HEIGHT:
#             print(f'picture is taller than screen')
#             # picture is wider than screen
#             if img_w > self.inky_what.WIDTH:
#                 print(f'picture is wider than screen')
#                 # picture mode (landscape)
#                 if rf_w > rf_h:
#                     print(f'picture is wider than taller')
#                     resize_factor = rf_w
#                 else:
#                     resize_factor = rf_h
#             else:
#                 print(f'picture is taller than wider')
#                 resize_factor = rf_h
#
#         elif img_w > self.inky_what.WIDTH:
#             resize_factor = rf_w
#
#         print(f'Resize Factor: {resize_factor}')
#         return resize_factor
#
#
#
#
#
#
# if __name__ == '__main__':
#     news = NewsBulletIn()
#     # news.draw_text()
#     news.draw_img()
#     # news.setup_widget()
