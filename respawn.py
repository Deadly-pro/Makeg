from copy import deepcopy
from random import randint
class Respawn:
    def __init__(self,**kwargs):
        self.newcopy=deepcopy(self)
        for key, value in kwargs.items():
            setattr(self, key ,value)     
    def update(self):
        self.newcopy.position=(randint(10,100),randint(1,10),randint(10,100))
        return self.newcopy