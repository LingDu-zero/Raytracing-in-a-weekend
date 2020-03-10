# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:18:30 2020

@author: asus
"""

from Vec3 import vec3
import numbers
import abc

class material(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered):
        pass

class hit_record():
    
    def __init__(self, t=0, p=vec3(0,0,0), normal=vec3(0,0,0), mat=0):
        if isinstance(p, vec3) and isinstance(normal, vec3) and isinstance(t, numbers.Real):
            self.record = [t, p, normal, mat]
        else:
            return NotImplemented

class hittable(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def hit(self, r, t_min, t_max, rec):
        pass

