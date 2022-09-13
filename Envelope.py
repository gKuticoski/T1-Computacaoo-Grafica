from Poligonos import Polygon
from Ponto import *
from Poligonos import *

class Envelope(Polygon):
    def __init__(self, min: Ponto, max: Ponto) -> None:
        super().__init__()
        self.min = min
        self.max = max
        self.insereVertice(min.x, min.y, 0)
        self.insereVertice(min.x, max.y, 0)
        self.insereVertice(max.x, max.y, 0)
        self.insereVertice(max.x, min.y, 0)
    
    def is_inside(self, pt: Ponto) -> bool:
        return (
            pt.x >= self.min.x and 
            pt.x < self.max.x and 
            pt.y >= self.min.y and 
            pt.y < self.max.y
        )
