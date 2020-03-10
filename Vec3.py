# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 21:59:43 2020

@author: asus
"""
import math
import numbers

class vec3():
    
    def __init__(self, e1, e2, e3):
        self.e = [float(e1), float(e2), float(e3)]
    
    def __repr__(self):
        return "[{}, {}, {}]".format(self.e[0], self.e[1], self.e[2])
    
    def length(self):
        return math.sqrt(self.e[0]*self.e[0]+self.e[1]*self.e[1]+self.e[2]*self.e[2])
        
    def make_unit_vector(self):
        k = 1.0/self.length()
        self.e[0] *= k
        self.e[1] *= k
        self.e[2] *= k
        
    def x(self):
        return self.e[0]
    
    def y(self):
        return self.e[1]
        
    def z(self):
        return self.e[2]
        
    def r(self):
        return self.e[0]
    
    def g(self):
        return self.e[1]
        
    def b(self):
        return self.e[2]
    
    def __add__(self, other):
        if isinstance(other, vec3):
            pairs = zip(self.e, other.e)
            vec = [a+b for a, b in pairs]
            return vec3(vec[0], vec[1], vec[2])
        else:
            return NotImplemented
    
    def __radd__(self, other):
        return self + other
    
    def __iadd__(self, other):
        return self + other
        
    def __sub__(self, other):
        if isinstance(other, vec3):
            pairs = zip(self.e, other.e)
            vec = [a-b for a, b in pairs]
            return vec3(vec[0], vec[1], vec[2])
        else:
            return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, vec3):
            pairs = zip(other.e, self.e)
            vec = [a-b for a, b in pairs]
            return vec3(vec[0], vec[1], vec[2])
        else:
            return NotImplemented
    
    def __isub__(self, other):
        return self - other
        
    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return vec3(self.e[0]*other, self.e[1]*other, self.e[2]*other)
        elif isinstance(other, vec3):
            pairs = zip(self.e, other.e)
            vec = [a*b for a, b in pairs]
            return vec3(vec[0], vec[1], vec[2])
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other
        
    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            return vec3(self.e[0]/other, self.e[1]/other, self.e[2]/other)
        elif isinstance(other, vec3):
            pairs = zip(self.e, other.e)
            vec = [a/b for a, b in pairs]
            return vec3(vec[0], vec[1], vec[2])
        else:
            return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, numbers.Real):
            return vec3(other/self.e[0], other/self.e[1], other/self.e[2])
        elif isinstance(other, vec3):
            pairs = zip(other.e, self.e)
            vec = [a/b for a, b in pairs]
            return vec3(vec[0], vec[1], vec[2])
        else:
            return NotImplemented
    
    def __itruediv__(self, other):
        return self / other
    
    def __getitem__(self, index):
        return self.e[index]
    
    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])
        
    def __pos__(self):
        return self.e
    
    def dot(v1, v2):
        if isinstance(v1, vec3) and isinstance(v2, vec3):
            return v1.e[0]*v2.e[0] + v1.e[1]*v2.e[1] + v1.e[2]*v2.e[2]
        else:
            return NotImplemented
    
    def cross(v1, v2):
        if isinstance(v1, vec3) and isinstance(v2, vec3):
            return vec3(v1.e[1] * v2.e[2] - v1.e[2] * v2.e[1],
                v1.e[2] * v2.e[0] - v1.e[0] * v2.e[2],
                v1.e[0] * v2.e[1] - v1.e[1] * v2.e[0])
        else:
            return NotImplemented
    
    def unit_vector(v):
        if isinstance(v, vec3):
            return v / v.length()
        else:
            return NotImplemented

