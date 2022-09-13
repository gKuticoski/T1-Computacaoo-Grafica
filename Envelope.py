from Poligonos import Polygon
from Ponto import *
from Poligonos import *

class Envelope(Polygon):
    def __init__(self, min: Ponto, max: Ponto) -> None:
        super().__init__()
        self.insereVertice(min.x, min.y, 0)
        self.insereVertice(min.x, max.y, 0)
        self.insereVertice(max.x, max.y, 0)
        self.insereVertice(max.x, min.y, 0)

