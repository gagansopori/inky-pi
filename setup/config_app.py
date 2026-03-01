from flask import Flask, request, render_template_string
import subprocess
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw

# We will update this import once you provide your core/Database.py
# from core.database import update_wifi_creds

app = Flask(__name__)

def draw_red_setup_screen(ssid="InkyPi_Setup", url="inkypi.local"):
    """Original logic from setup_banner.py integrated here."""
    try:
        display = auto()
        img = Image.new("P", (display.WIDTH, display.HEIGHT), display.RED)
        draw = ImageDraw.Draw(img)
        try:
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            font_reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            font_bold = font_reg = ImageFont.load_default()

        header = "SETUP YOUR inkyPi"
        step1 = f"1. Connect to SSID: {ssid}"
        step2 = f"2. Go to: http://{url}"

        def get_center_x(text, font):
            bbox = draw.textbbox((0, 0), text, font=font)
            return (display.WIDTH - (bbox[2] - bbox[0])) // 2

        draw.text((get_center_x(header, font_bold), 25), header, fill=display.WHITE, font=font_bold)
        draw.line((20, 50, display.WIDTH-20, 50), fill=display.WHITE, width=2)
        draw.text((get_center_x(step1, font_reg), 70), step1, fill=display.WHITE, font=font_reg)
        draw.text((get_center_x(step2, font_reg), 100), step2, fill=display.WHITE, font=font_reg)

        display.set_image(img)
        display.show()
    except Exception as e: print(f"Display Error: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; padding: 40px 20px; background: #fafafa; color: #333; }
        .card { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h2 { margin-top: 0; color: #d63031; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 14px; background: #2d3436; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h2>InkyPi Setup</h2>
        <form method="POST">
            <label>Wi-Fi Name (SSID)</label>
            <input type="text" name="ssid" required>
            <label>Password</label>
            <input type="password" name="password" required>
            <button type="submit">Update & Reboot</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid, pwd = request.form.get('ssid'), request.form.get('password')
        update_wifi_creds(ssid, pwd) # To be enabled after merge
        cmd = f"sleep 2 && nmcli device wifi connect '{ssid}' password '{pwd}' && sudo reboot"
        subprocess.Popen(cmd, shell=True)
        return "<h2>Configuring...</h2><p>The Pi is rebooting to connect to your network.</p>"
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    draw_red_setup_screen()
    app.run(host='0.0.0.0', port=80)