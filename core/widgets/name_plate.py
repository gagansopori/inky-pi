import os
from .base import Widget, WidgetState

class NamePlateMini(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((x + 20, y + 40), data['name'].upper(), fill=1) # Black
        draw.text((x + 20, y + 80), data['title'], fill=2) # Red

class NamePlateMaxi(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((20, 50), data['name'].upper(), fill=1)
        draw.text((20, 130), data['title'], fill=1)
        draw.text((20, 200), data['company'], fill=2)


class NamePlateWidget(Widget):
    def __init__(self, asset_path="/home/pi/inky-pi/assets/identity.md"):
        super().__init__("NamePlate")
        self.asset_path = asset_path

    def fetch_data(self):
        data = {"name": "UNKNOWN", "title": "ENGINEER", "company": "CORP"}
        try:
            if os.path.exists(self.asset_path):
                with open(self.asset_path, 'r') as f:
                    for line in f:
                        if ':' in line:
                            key, val = line.split(':', 1)
                            data[key.strip().lower()] = val.strip()
        except Exception as e:
            print(f"Error reading identity asset: {e}")

        self.data = data