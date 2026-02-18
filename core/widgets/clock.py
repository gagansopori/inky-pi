from datetime import datetime
from .base import Widget, WidgetState

class ClockMini(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((x + 40, y + 50), data['time'], fill=1)

class ClockMaxi(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((80, 110), data['time'], fill=1)

class ClockWidget(Widget):
    def fetch_data(self):
        self.data = {"time": datetime.now().strftime("%H:%M")}