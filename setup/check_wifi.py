import socket
import sys
import time

try:
    from inky.auto import auto
    from PIL import Image, ImageFont, ImageDraw
    HAS_DISPLAY = True
except ImportError:
    HAS_DISPLAY = False

def display_status(message):
    """Simple grayscale update for the boot process."""
    if not HAS_DISPLAY: return
    try:
        display = auto()
        img = Image.new("P", (display.WIDTH, display.HEIGHT))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((20, 20), "INKY-PI BOOT", display.BLACK, font=font)
        draw.text((20, 50), f"> {message}", display.BLACK, font=font)
        display.set_image(img)
        display.show()
    except Exception: pass

def is_connected():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error:
        return False

def main():
    if is_connected(): sys.exit(0)
    display_status("Connecting to WiFi...")
    for i in range(60):
        if is_connected(): sys.exit(0)
        time.sleep(1)
    sys.exit(1)

if __name__ == "__main__":
    main()