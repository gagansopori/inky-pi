from abc import ABC, abstractmethod
from PIL import ImageDraw

class WidgetState(ABC):
    @abstractmethod
    def render(self, draw: ImageDraw, x: int, y: int, w: int, h: int, data: dict):
        pass

class Widget(ABC):
    def __init__(self, name: str):
        self.name = name
        self.state: WidgetState = None
        self.data = {}

    def set_state(self, state: WidgetState):
        self.state = state

    @abstractmethod
    def fetch_data(self):
        pass

    def draw(self, draw: ImageDraw, x: int, y: int, w: int, h: int):
        if self.state:
            self.state.render(draw, x, y, w, h, self.data)