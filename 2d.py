from copy import deepcopy
from collections import defaultdict
from math import pi
from time import time

from PIL import Image, ImageDraw

G = 100

TIMEDELTA = 1/2

w = h = 256

img = Image.new("RGB", (w,h))
draw = ImageDraw.Draw(img)

steps = 255*2

ID = 0#should never be 0 because of if checks

def nextid():
    global ID
    ID += 1
    return ID

distanceCache = {}

def distance(a, b):
    global distanceCache

    key = (a.id, b.id) if a.id < b.id else (b.id, a.id)

    if key in distanceCache:
        return distanceCache[key]

    dist = ((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)**0.5

    distanceCache[key] = dist

    return dist


class Mass:
    def __init__(self, m, x, y, z):

        self.id = nextid()

        self.status = None

        self.x = x
        self.y = y
        self.z = z

        self.m = m
        self.r = (m*3/4/pi)**(1/3)

        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.ax = 0
        self.ay = 0
        self.az = 0


    def gravity(self, b):
        dist = distance(self, b)
        if dist < self.r + b.r:
            self.status = b.id
            return

        if dist > 1000:
            self.status = "escape"
            return

        dx = b.x-self.x
        dy = b.y-self.y
        dz = b.z-self.z

        force = G*b.m/dist**3

        self.ax += force * dx
        self.ay += force * dy
        self.az += force * dz

for x in range(-w//2, w//2):
    print(x)
    for y in range(-h//2, h//2):

        ID = 0
        masses = [Mass(10, -50, 0, 0), Mass(10, 50, 0, 0)]
        masses[0].vy = 8
        masses[1].vy = -8

        masses.append(Mass(1, x, y, 0))

        for step in range(steps):
            distanceCache = {}
            newmasses = []
            for mi, mass in enumerate(masses):
                nm = deepcopy(mass)

                nm.ax = 0
                nm.ay = 0
                nm.az = 0

                for mass2 in masses:
                    if mass == mass2:
                        continue
                    nm.gravity(mass2)

                nm.vx += nm.ax
                nm.vy += nm.ay
                nm.vz += nm.az

                nm.x += nm.vx * TIMEDELTA
                nm.y += nm.vy * TIMEDELTA
                nm.z += nm.vz * TIMEDELTA

                newmasses.append(nm)

            masses = newmasses

            if masses[-1].status == "escape":
                color = (100,100,100)
                break
            elif masses[-1].status is not None:
                color = [(0,255,0), (0,0,255)][masses[-1].status-1]
                break

        if step == steps-1:
            color = (50,50,50)

        img.putpixel((x+w//2,y+h//2), color)


img = img.resize((img.size[0]*2, img.size[1]*2), Image.NEAREST)

img.save(f"{int(time()*1000)}.png")
img.show()
