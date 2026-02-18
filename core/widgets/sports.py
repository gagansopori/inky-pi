import requests

from .base import Widget, WidgetState

class SportsMini(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((x + 10, y + 30), f"{data['home']} {data['h_score']}", fill=1)
        draw.text((x + 10, y + 70), f"{data['away']} {data['a_score']}", fill=2)

class SportsMaxi(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((40, 60), f"{data['home']} vs {data['away']}", fill=1)
        draw.text((40, 140), f"{data['h_score']} - {data['a_score']}", fill=2)


class SportsWidget(Widget):
    def __init__(self, config_path="/home/pi/inky-pi/assets/sports_config.md"):
        super().__init__("Sports")
        self.config_path = config_path
        self.rotation_index = 1  # To cycle through MAXI_URL_1 to 4

    def _get_urls(self):
        urls = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                for line in f:
                    if ':' in line:
                        k, v = line.split(':', 1)
                        urls[k.strip().upper()] = v.strip()
        return urls

    def fetch_data(self):
        urls = self._get_urls()

        # Determine which URL to hit based on State
        if isinstance(self.state, SportsMini):  # Logic depends on current state
            target_url = urls.get('MINI_URL')
        else:
            target_url = urls.get(f'MAXI_URL_{self.rotation_index}')
            # Increment for next time
            self.rotation_index = 1 if self.rotation_index >= 4 else self.rotation_index + 1

        try:
            r = requests.get(target_url, timeout=5)
            game = r.json()['events'][0]
            comp = game['competitions'][0]
            self.data = {
                "home": comp['competitors'][0]['team']['abbreviation'],
                "h_score": comp['competitors'][0]['score'],
                "away": comp['competitors'][1]['team']['abbreviation'],
                "a_score": comp['competitors'][1]['score'],
                "status": game['status']['type']['shortDetail']
            }
        except:
            self.data = {"home": "N/A", "h_score": "-", "away": "N/A", "a_score": "-", "status": "No Game"}