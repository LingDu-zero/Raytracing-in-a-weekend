# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:26:11 2020

@author: asus
"""

from Hit import hittable
from Vec3 import vec3
import math

class sphere(hittable):
    
    def __init__(self, cen, r, mat):
        self.center = cen
        self.radius = r
        self.mat = mat
        
    def hit(self, r, t_min, t_max, rec):
        oc = r.origin() - self.center
        a = vec3.dot(r.direction(), r.direction())
        b = vec3.dot(oc, r.direction())
        c = vec3.dot(oc, oc) - self.radius*self.radius
        discriminant = b*b - a*c
        if discriminant > 0:
            temp = (-b - math.sqrt(discriminant)) / a
            if temp < t_max and temp > t_min:
                rec.record[0] = temp
                rec.record[1] = r.point_at_parameter(rec.record[0])
                rec.record[2] = (rec.record[1] - self.center) / self.radius
                rec.record[3] = self.mat
                return True

            temp = (-b + math.sqrt(discriminant)) / a
            if temp < t_max and temp > t_min:
                rec.record[0] = temp
                rec.record[1] = r.point_at_parameter(rec.record[0])
                rec.record[2] = (rec.record[1] - self.center) / self.radius
                rec.record[3] = self.mat
                return True

        return False
