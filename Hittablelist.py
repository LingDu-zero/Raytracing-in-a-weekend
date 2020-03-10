# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:48:13 2020

@author: asus
"""

from Hit import hittable

class hittable_list(hittable):
    
    def __init__(self, l):
            self.list = l
    
    def hit(self, r, t_min, t_max, rec):
        temp_rec = rec
        hit_anything = False
        closest_so_far = t_max
        for i in self.list:
            if i.hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.record[0]
                rec = temp_rec
        return hit_anything