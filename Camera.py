# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 18:38:57 2020

@author: asus
"""

from Vec3 import vec3
from Ray import ray
import math
import random

def random_in_unit_disk():
    while True:
        p = 2.0*vec3(random.random(), random.random(), 0) - vec3(1, 1, 0)
        if vec3.dot(p, p) < 1:
            break
    return p

class camera():
    
    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
        self.lens_radius = aperture / 2
        theta = vfov * math.pi / 180
        half_height = math.tan(theta/2)
        half_width = aspect * half_height
        self.origin = lookfrom
        self.w = vec3.unit_vector(lookfrom - lookat)
        self.u = vec3.unit_vector(vec3.cross(vup, self.w))
        self.v = vec3.cross(self.w, self.u)
        self.lower_left_corner = self.origin - half_width*focus_dist*self.u - half_height*focus_dist*self.v - focus_dist*self.w
        self.horizontal = 2*half_width*focus_dist*self.u
        self.vertical = 2*half_height*focus_dist*self.v
    
    def get_ray(self, s, t):
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u*rd.x() + self.v*rd.y()
        return ray(self.origin + offset, self.lower_left_corner + s*self.horizontal + t*self.vertical - self.origin - offset)
