#Title: LAB3
#Author: ac2255
#Instructor: Jansen Orfan

class dtNode:
    __slots__ = "value", "left", "right"

    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

    
    