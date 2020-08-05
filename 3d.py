from copy import deepcopy
from collections import defaultdict
from math import pi
from time import time

G = 1

ID = 0#should never be 0 because of if checks

def nextid():
    global ID
    ID += 1
    return ID

class Mass:
    def __init__(self, m, x, y, z):

        self.id = nextid()

        self.status = None

        self.x = x
        self.y = y
        self.z = z

        self.m = m
        self.r = (m*3/4/pi)**0.3
        print(self.r)

        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.ax = 0
        self.ay = 0
        self.az = 0

        self.ix = 0
        self.iy = 0
        self.iz = 0

    def distance(self, b):
        return ((self.x - b.x)**2 + (self.y - b.y)**2 + (self.z - b.z)**2)**0.5

    def gravity(self, b):
        dist = self.distance(b)
        if dist < self.r + b.r:
            self.status = b.id
            return

        if dist > 1000:
            self.status = "escape"
            return

        dx = b.x-self.x
        dy = b.y-self.y
        dz = b.z-self.z
        force = G*self.m*b.m/dist**3
        self.ix += force * dx
        self.iy += force * dy
        self.iz += force * dz



"""
for x in range(-5, 5):
    for y in range(-5, 5):
        masses.append(Mass(1, x, y, 0))
"""

from PIL import Image, ImageDraw

w = h = 64

img = Image.new("RGB", (w,h))
draw = ImageDraw.Draw(img)

steps = 100

#paths = defaultdict(list)

for x in range(-w//2, w//2):
    for y in range(-h//2, h//2):

        print(x,y)

        ID = 0
        masses = [Mass(100, -50, 0, 0), Mass(100, 50, 0, 0)]
        masses[0].vy = 8
        masses[1].vy = -8

        masses.append(Mass(1, x, y, 0))

        for step in range(steps):
            newmasses = []
            for mi, mass in enumerate(masses):
                nm = deepcopy(mass)

                nm.ix = 0
                nm.iy = 0
                nm.iz = 0

                for mass2 in masses:
                    if mass == mass2:
                        continue
                    nm.gravity(mass2)

                nm.vx += nm.ax + nm.ix
                nm.vy += nm.ay + nm.iy
                nm.vz += nm.az + nm.iz

                nm.x += nm.vx
                nm.y += nm.vy
                nm.z += nm.vz

                newmasses.append(nm)

                #paths[mi].append([nm.x, nm.y])

            masses = newmasses

            if masses[-1].status == "escape":
                color = (step,100,100)
                break
            elif masses[-1].status is not None:
                print(masses[-1].status)
                color = [(0,255,0), (0,0,255)][masses[-1].status-1]
                break

        if step == steps-1:
            color = (30,30,30)

        img.putpixel((x+w//2,y+h//2), color)



"""
for path in paths.values():
    #print(path)
    draw.line([(xy[0]+w//2,xy[1]+h//2) for xy in path])
"""

img = img.resize((img.size[0]*2, img.size[1]*2))

img.save(f"{int(time()*1000)}.png")
img.show()

#print([[m.x, m.y, m.z] for m in masses])
