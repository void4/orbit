#Using https://physics.stackexchange.com/questions/332456/can-you-have-a-giraffe-shaped-black-hole
import pygame
from time import sleep
from math import sin, cos, pi
from copy import deepcopy

pygame.init()
pygame.display.set_caption("Falling")

W = H = 1024

screen = pygame.display.set_mode((W,H))

color = (0,0,0)

running = True

timespeed = 1

bx = W//2
by = H//2
bm = 1000000

pm = 1
px = W//2+200
py = H//2
pvx = 0
pvy = 0
pax = 0
pay = 0

c = 10

G = 0.1

tick = 0
ticks_per_draw = 100

scale = 100
timescale = 100

def acceleration(m1,m2,r):
	return G*m1*m2/r**2

def escapevelocity(m, r):
	return (2*G*m/r)**0.5

def timedilation(ev):
	return (1-(ev/c)**2)**0.5

def eventhorizon(m):
	return 2*G*m/c**2



lastdist = scale*px*10

data = []

start = False
startick = None

velocities = []

while running:

	drawcycle = tick%ticks_per_draw == 0
	if tick % 10000 == 0:
		print(tick)

	dist = abs((bx-px)*scale)

	if start:
		pax = 0
		pay = 0
		sr = eventhorizon(bm)
		#pvx += pax*td
		pvx = -(1-sr/dist)*(sr/dist)**0.5#/scale
		pvy += pay

		if drawcycle:
			velocities.append(((tick-startick)/100,100+pvx*100))

		px += pvx/timescale
		py += pvy

		print(tick, px, pvx)

	if drawcycle:
		screen.fill(color)
		pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(int(px-2), int(py-2), 5, 5))
		pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(bx-2, by-2, 5, 5))
		try:
			pygame.draw.circle(screen, (255,255,255), (bx,by), int(eventhorizon(bm)/scale), 1)
		except ValueError:
			pass

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_LEFT:
					timespeed *= 2
				elif key == pygame.K_RIGHT:
					timespeed /= 2
				elif key == pygame.K_s:
					start = True
					startick = tick


	if drawcycle:
		if start and len(velocities) > 1:
			pygame.draw.lines(screen, (255,255,255), False, velocities)
		pygame.display.flip()
		#sleep(0.01)

	tick += 1

"""
import numpy as np
import matplotlib.pyplot as plt
ys = [d[1] for d in data]
#plt.plot(ys)
plt.plot(np.diff(ys))
plt.show()
"""
