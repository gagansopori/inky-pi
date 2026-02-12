from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw


def update_status_setup(ssid, url="inkypi.local"):
    """
    Renders a Red background with Centered White text for Setup Mode.
    """
    try:
        inky_display = auto()
        # Initialize image with RED background
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.RED)
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            font_reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            font_bold = ImageFont.load_default()
            font_reg = ImageFont.load_default()

        # Content to display
        header = "SETUP YOUR inkyPi"
        step1 = f"1. Connect to SSID: {ssid}"
        step2 = f"2. Go to: http://{url}"

        # Helper to get horizontal center position
        def get_center_x(text, font):
            # textbbox returns (left, top, right, bottom)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            return (inky_display.WIDTH - text_width) // 2

        # 1. Position Header
        header_x = get_center_x(header, font_bold)
        draw.text((header_x, 25), header, fill=inky_display.WHITE, font=font_bold)

        # 2. Draw a centered separator line
        line_w = int(inky_display.WIDTH * 0.8)
        line_x_start = (inky_display.WIDTH - line_w) // 2
        draw.line((line_x_start, 50, line_x_start + line_w, 50), fill=inky_display.WHITE, width=2)

        # 3. Position Step 1
        s1_x = get_center_x(step1, font_reg)
        draw.text((s1_x, 70), step1, fill=inky_display.WHITE, font=font_reg)

        # 4. Position Step 2
        s2_x = get_center_x(step2, font_reg)
        draw.text((s2_x, 100), step2, fill=inky_display.WHITE, font=font_reg)

        # Write to hardware
        inky_display.set_image(img)
        inky_display.show()

    except Exception as e:
        print(f"Display Error: {e}")


if __name__ == "__main__":
    update_status_setup("InkyPi_Setup")