from __future__ import division
from ast import Return
from Poligonos import *
from Envelope import *
from Ponto import *

NroDiv = 0
class QuadTree():
    def __init__(self, boundary: Envelope, capacity: int) -> None:
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.testes = 0
        self.division = 0

        self.southEast = None
        self.northWest = None
        self.northEast = None
        self.southWest = None
    
    def insert_point(self, pt: Ponto) -> bool:
        if not self.boundary.is_inside(pt):
            return False
        
        if len(self.points) < self.capacity:
            self.points.append(pt)
            return True
        
        if not self.is_divided():
            self.divide()
            for p in self.points:
                self.insert_in_children(p)
            
            self.points = []
        
        self.insert_in_children(pt)
        return True
    
    def is_divided(self) -> bool:
        return self.northWest is not None
    
    def divisions(self) -> int:
        if self.is_divided():
            return self.northEast.divisions() + self.northWest.divisions() + self.southEast.divisions() + self.southWest.divisions()
        
        return 1

    def divide(self) -> None:
        min = self.boundary.min
        max = self.boundary.max
        middle = Ponto(min.x +(max.x-min.x) * 0.5, min.y + (max.y-min.y) * 0.5)
        middle_left = Ponto(min.x, min.y + (max.y-min.y) * 0.5)
        middle_top = Ponto(min.x + (max.x-min.x) * 0.5, max.y)
        middle_right= Ponto(max.x, min.y + (max.y-min.y) * 0.5)
        middle_bottom = Ponto(min.x + (max.x-min.x) * 0.5, min.y)

        self.southWest = QuadTree(Envelope(copy.deepcopy(min), copy.deepcopy(middle)), self.capacity)
        self.northWest = QuadTree(Envelope(copy.deepcopy(middle_left), copy.deepcopy(middle_top)), self.capacity)
        self.northEast = QuadTree(Envelope(copy.deepcopy(middle), copy.deepcopy(max)), self.capacity)
        self.southEast = QuadTree(Envelope(copy.deepcopy(middle_bottom), copy.deepcopy(middle_right)), self.capacity)
        # self.divisions += 1
        # print("divisions: ", self.divisions) =7
    
    def insert_in_children(self, pt: Ponto) -> bool:
        self.southEast.insert_point(pt)
        self.northWest.insert_point(pt)
        self.northEast.insert_point(pt)
        self.southWest.insert_point(pt)

    def desenha_quad_tree(self):
        global NroDiv
        self.boundary.desenhaPoligono()
        #print("divisions antes: ", self.divisions)
        #self.divisions += 1
        NroDiv += 1
        if self.is_divided():
            self.southEast.desenha_quad_tree()
            #self.divisions += 1
            self.northWest.desenha_quad_tree()
            #self.divisions += 1
            self.northEast.desenha_quad_tree()
            #self.divisions += 1
            self.southWest.desenha_quad_tree()
            #self.divisions += 1
        #self.divisions += self.divisions
       # print("divisions depois: ", self.divisions)
    

    def getNroDiv(self):
        global NroDiv
        return NroDiv
    
    def is_overlapping(self, min_rect: Ponto, max_rect: Ponto):
        if self.boundary.min.x > max_rect.x or min_rect.x > self.boundary.max.x:
            return False

        if self.boundary.min.y > max_rect.y or min_rect.y > self.boundary.max.y:
            return False

        return True
    
    def intersecao(self, rect: Envelope, pool: Polygon) -> bool:
        min_rect, max_rect = rect.getLimits()
        #self.testes += 1
        if not self.is_overlapping(min_rect, max_rect):
            return False

        for V in self.points:
            pool.insereVertice(V.x, V.y, V.z)
        

        #self.testes = 0
        if self.is_divided():
            self.northWest.intersecao(rect, pool)
            self.southEast.intersecao(rect, pool)
            self.northEast.intersecao(rect, pool)
            self.southWest.intersecao(rect, pool)
        
            #self.testes += self.northWest.testes +  self.southEast.testes + self.northEast.testes + self.southWest.testes
            #print("testes: ", self.testes)
            return True
        
        #self.testes += 1
        
        self.boundary.desenhaPoligono()
        return True
