from datetime import datetime
from .base import Widget, WidgetState

class CalendarMini(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((x + 40, y + 50), data['time'], fill=1)

class CalendarMaxi(WidgetState):
    def render(self, draw, x, y, w, h, data):
        draw.text((80, 110), data['time'], fill=1)

class CalendarWidget(Widget):
    def fetch_data(self):
        self.data = {"time": datetime.now().strftime("%H:%M")}