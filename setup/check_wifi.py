import subprocess
import sys
import time
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw

def display_message(message):
    try:
        inky_display = auto()
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((10, 10), "SYSTEM BOOT", inky_display.BLACK, font=font)
        draw.text((10, 30), message, inky_display.BLACK, font=font)
        inky_display.set_image(img)
        inky_display.show()
    except:
        pass # Don't crash the boot if display is unplugged

def check_ping():
    try:
        # Ping Google DNS once, wait max 2 seconds for response
        subprocess.check_call(['ping', '-c', '1', '-W', '2', '8.8.8.8'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Start the 60-second loop
display_message("Checking WiFi...")
for i in range(60):
    if check_ping():
        sys.exit(0) # Success!
    time.sleep(1)

sys.exit(1) # Failure after 60 seconds