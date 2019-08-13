import numpy as np
class Base(object):
    def __init__(self):
        self._width = 300
        self._area = self._width*self._width
        
    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, width):
        self._width = width
        self._area = width*width

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        raise ValueError()
    
    
if __name__ == "__main__":
    b=Base()
    b.width=200.0
    print(b.width)
    print(b.area)
    b.area=400.0
