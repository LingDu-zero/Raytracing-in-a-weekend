# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:51:21 2020

@author: asus
"""


from Vec3 import vec3
from Ray import ray
from Hittablelist import hittable_list
from Hit import hit_record, material
from Sphere import sphere
from Camera import camera
import random
import math

'''
def hit_sphere(center, radius, r):
    if isinstance(center, vec3) and isinstance(r, ray):
        oc = r.origin() - center
        a = vec3.dot(r.direction(), r.direction())
        b = 2.0 * vec3.dot(oc, r.direction())
        c = vec3.dot(oc, oc) - radius*radius
        discriminant = b*b - 4*a*c
        if discriminant<0:
            return -1.0
        else:
            return (-b-math.sqrt(discriminant)) / (2.0*a)
    else:
        return NotImplemented
'''

def random_in_unit_sphere():
    while True:
        p = 2.0 * vec3(random.random(), random.random(), random.random()) - vec3(1, 1, 1)
        if p.length() < 1.0:
            break
    return p

def reflect(v, n):
    if isinstance(v, vec3) and isinstance(n, vec3):
        return v - 2*vec3.dot(v, n)*n
    else:
        return NotImplemented

def refract(v, n, ni_over_nt):
    uv = vec3.unit_vector(v)
    dt = vec3.dot(uv, n)
    discriminant = 1.0 - ni_over_nt*ni_over_nt*(1-dt*dt)
    refracted = vec3(0, 0, 0)
    if discriminant > 0:
        refracted = ni_over_nt*(uv - n*dt) - n*math.sqrt(discriminant)
        return True, refracted
    else:
        return False, refracted

def schlick(cosine, ref_idx):
    r0 = (1-ref_idx)/(1+ref_idx)
    r0 = r0*r0
    return r0 + (1-r0)*pow((1 - cosine),5)

class dielectric(material):
    
    def __init__(self, ri):
        self.ref_idx = ri
        
    def scatter(self, r_in, rec):
        reflected = reflect(r_in.direction(), rec.record[2])
        attenuation = vec3(1.0, 1.0, 1.0)
        
        if (vec3.dot(r_in.direction(), rec.record[2]) > 0):
            outworld_normal = -rec.record[2]
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * vec3.dot(r_in.direction(), rec.record[2]) / r_in.direction().length()
        else:
            outworld_normal = rec.record[2]
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -vec3.dot(r_in.direction(), rec.record[2]) / r_in.direction().length()
        
        isok, refracted = refract(r_in.direction(), outworld_normal, ni_over_nt)
        if isok:
            reflect_prob = schlick(cosine, self.ref_idx)   
        else:
            reflect_prob = 1.0
            
        if random.random() < reflect_prob:
            scattered = ray(rec.record[1], reflected)
        else:
            scattered = ray(rec.record[1], refracted)
            
        return True, scattered, attenuation
            

class metal(material):
    
    def __init__(self, a, f):
        if isinstance(a, vec3):
            self.albedo = a
            if f < 1:
                self.fuzz = f
            else:
                self.fuzz = 1
        else:
            return NotImplemented
    
    def scatter(self, r_in, rec):
        reflected = reflect(vec3.unit_vector(r_in.direction()), rec.record[2])
        scattered = ray(rec.record[1], reflected + self.fuzz*random_in_unit_sphere())
        isok = (vec3.dot(scattered.direction(), rec.record[2]) > 0)
        return isok, scattered, self.albedo

class lambertian(material):
    
    def __init__(self, a):
        if isinstance(a, vec3):
            self.albedo = a
        else:
            return NotImplemented
    
    def scatter(self, r_in, rec):
        target = rec.record[1] + rec.record[2] + random_in_unit_sphere()
        scattered = ray(rec.record[1], target - rec.record[1])
        return True, scattered, self.albedo
        
        
def random_scene():
    hlist = []
    hlist.append(sphere(vec3(0,-1000,0), 1000, lambertian(vec3(0.5, 0.5, 0.5))))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = vec3(a+0.9*random.random(), 0.2, b+0.9*random.random())
            if (center - vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    hlist.append(sphere(center, 0.2, lambertian(vec3(random.random(), random.random(), random.random()))))
                elif choose_mat < 0.95:
                    hlist.append(sphere(center, 0.2, metal(vec3(0.5*(1+random.random()), 0.5*(1+random.random()), 0.5*(1+random.random())), 0.5*random.random())))
                else:
                    hlist.append(sphere(center, 0.2, dielectric(1.5)))
    
    hlist.append(sphere(vec3(0, 1, 0), 1.0, dielectric(1.5)))
    hlist.append(sphere(vec3(-4, 1, 0), 1.0, lambertian(vec3(0.4, 0.2, 0.1))))
    hlist.append(sphere(vec3(4, 1, 0), 1.0, metal(vec3(0.7, 0.6, 0.5), 0.0)))
    return hittable_list(hlist)

def color(r, world, depth):
    if isinstance(r, ray):
        infinity = float('inf')
        rec = hit_record()
        if world.hit(r, 0.001, infinity, rec):
            isscatter, s, a = rec.record[3].scatter(r, rec)
            if depth < 50 and isscatter:
                return a * color(s, world, depth+1)
            else:
                return vec3(0, 0, 0)
        else:
            unit_direction = vec3.unit_vector(r.direction())
            t = 0.5*(unit_direction.y() + 1.0)
            return (1.0-t)*vec3(1.0, 1.0, 1.0) + t*vec3(0.5, 0.7, 1.0)
    else:
        return NotImplemented

if __name__ == '__main__':
    file = r'.\out.ppm'
    
    nx = 200
    ny = 100
    ns = 100
    
    world = random_scene()

    lookfrom = vec3(11, 5, 2)
    lookat = vec3(0, 0, -1)
    dist_to_focus = (lookfrom - lookat).length()
    aperture = 0.05
    
    with open(file, 'w') as p:
        p.write("P3\n")
        p.write("{} {}\n".format(nx, ny))
        p.write("255\n")
    
        for y in range(ny):
            print(y)
            for x in range(nx):
                col = vec3(0, 0, 0)
                cam = camera(lookfrom, lookat, vec3(0,1,0), 25, float(nx)/float(ny), aperture, dist_to_focus)
                for z in range(ns):
                    u = float(x + random.random())/float(nx)
                    v = float(99-y + random.random())/float(ny)
                    r = cam.get_ray(u, v)
                    col += color(r, world, 0)
                col /= float(ns)
                col = vec3(math.sqrt(col[0]), math.sqrt(col[1]), math.sqrt(col[2]))
                
                ir = int(255.99*col[0])
                ig = int(255.99*col[1])
                ib = int(255.99*col[2])
                p.write("{} {} {}\n".format(ir, ig, ib))
