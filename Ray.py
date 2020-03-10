# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 19:37:15 2020

@author: asus
"""

from Vec3 import vec3

class ray():
    
    def __init__(self, a, b):
        if isinstance(a, vec3) and isinstance(b, vec3):
            self.A = a
            self.B = b
        else:
            return NotImplemented
    
    def origin(self):
        return self.A
    
    def direction(self):
        return self.B
    
    def point_at_parameter(self, t):
        return self.A + self.B * t
