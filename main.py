import pygame
from time import sleep
from math import sin, cos, pi

pygame.init()
pygame.display.set_caption("XXX")

W = H = 1024

screen = pygame.display.set_mode((W,H))

color = (50, 50, 200)

sm = 1
sx = W//2-15
sy = H//2+20
svx = 0.2
svy = 0
sax = 0
say = 0
sr = 0
ROT_RATE = 2*pi/100

FUTURESTEPS = 10000

G = 1

gravities = [(W//2,H//2,0.01), (W//2+100,H//2+100,0.01)]

def cap(c, v):
	if 0 <= v < c:
		return c
	elif -c < v < 0:
		return -c
	else:
		return v

def gravity(m,x,y,g):
	dx = cap(1,x-g[0])
	dy = cap(1,y-g[1])
	#print(dx,dy)
	dist = (dx**2+dy**2)**0.5
	#print(dist)
	#dist = max(dist, 1)

	return -dx*G*m*g[2]/dist**2, -dy*G*m*g[2]/dist**2

i = 0
running = True

while running:

	drawcycle = i%100 == 0

	if drawcycle:
		screen.fill(color)
		pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sx, sy, 40, 30))

		for g in gravities:
			pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(g[0],g[1],10,10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			key = event.key
			if key == pygame.K_LEFT:
				sr -= ROT_RATE
			elif key == pygame.K_RIGHT:
				sr += ROT_RATE

	x = sx
	y = sy
	vx = svx
	vy = svy

	r = sr

	path = []

	steps = FUTURESTEPS if drawcycle else 1
	for f in range(steps):
		ax = 0#sax
		ay = 0#say

		for grav in gravities:
			dax, day = gravity(sm,x,y,grav)
			ax += dax#(grav[2]/cap(1, grav[0]-x))**2
			ay += day#(grav[2]/cap(1, grav[1]-y))**2

		vx += ax
		vy += ay

		x += vx
		y += vy

		path.append((x,y))

		if f == 0:
			print(ax,ay)
			sx = x
			sy = y
			svx = vx
			svy = vy
			sax = ax
			say = ay
			sr = r


	if drawcycle:
		pygame.draw.lines(screen, (255,255,255), False, path)

		pygame.display.flip()
		sleep(0.01)

	i += 1
