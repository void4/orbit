import pygame
from time import sleep
from math import sin, cos, pi
from copy import deepcopy

pygame.init()
pygame.display.set_caption("XXX")

W = H = 1024

screen = pygame.display.set_mode((W,H))

color = (50, 50, 200)

sx = W//2-15
sy = H//2+20

ROT_RATE = 2*pi/100

FUTURESTEPS = 1000

G = 0.01

class Mass:
	def __init__(self, m, x, y):
		self.m = m
		self.x = x
		self.y = y
		self.vx = 0
		self.vy = 0
		self.ax = 0
		self.ay = 0
		self.r = 0

masses = [Mass(0.0001,sx,sy), Mass(0.001, W//2,H//2), Mass(0.001, W//2+100,H//2+100)]

masses[1].vx = 0.005
masses[2].vx = -0.005

player = masses[0]

def cap(c, v):
	if 0 <= v < c:
		return c
	elif -c < v < 0:
		return -c
	else:
		return v


def gravity(ma,mb):
	dx = cap(1,ma.x-mb.x)
	dy = cap(1,ma.y-mb.y)

	dist = (dx**2+dy**2)**0.5

	return -dx*G*ma.m*mb.m/dist**2, -dy*G*ma.m*mb.m/dist**2

tick = 0
running = True

while running:

	drawcycle = tick%100 == 0

	if drawcycle:
		screen.fill(color)
		pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player.x, player.y, 40, 30))

		for mass in masses:
			if mass != player:
				pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(mass.x,mass.y,10,10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			key = event.key
			if key == pygame.K_LEFT:
				player.r -= ROT_RATE
			elif key == pygame.K_RIGHT:
				player.r += ROT_RATE

	x = player.x
	y = player.y
	vx = player.vx
	vy = player.vy

	r = player.r

	path = []

	steps = FUTURESTEPS if drawcycle else 1

	futuremasses = [deepcopy(mass) for mass in masses]

	# TODO do not recalculate same steps!
	for f in range(steps):

		for ma in futuremasses:
			for mb in futuremasses:
				if ma == mb:
					continue
				dax, day = gravity(ma,mb)
				ma.ax += dax
				ma.ay += day

			ma.vx += ma.ax
			ma.vy += ma.ay

			ma.x += ma.vx
			ma.y += ma.vy

		path.append((futuremasses[0].x,futuremasses[0].y))

		if f == 0:
			for i,ma in enumerate(futuremasses):
				for key in "x y vx vy ax ay r".split():
					setattr(masses[i], key, getattr(ma,key))


	if drawcycle:
		if len(path) > 1:
			pygame.draw.lines(screen, (255,255,255), False, path)

		pygame.display.flip()
		sleep(0.01)

	tick += 1
