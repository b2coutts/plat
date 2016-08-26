#!/usr/bin/env python2

import pygame
import params
from util import *
from Level import *
from Ent import Ent

blockimg = pygame.image.load("img/block.png").convert()
kbimg    = pygame.image.load("img/kb.png").convert()

bwidth = 20
w,h = params.SCREEN_SIZE

def circle_beh(plat,frame):
    t = frame * (2*math.pi)/(60*10.0)
    plat.speed = [math.cos(t), math.sin(t)]

# obstacles
border  = [Ent(-bwidth, -bwidth, w + 2*bwidth, bwidth),\
           Ent(-bwidth, -bwidth, bwidth, h + 2*bwidth),\
           Ent(w, -bwidth, bwidth, h + 2*bwidth),\
           Ent(-bwidth, h, w + 2*bwidth, bwidth)]
vborder = [mkplat(0, 0, 40, 1), mkplat(0, 0, 1, 30), mkplat(0, 580, 40, 1),\
           mkplat(780, 0, 1, 30)]
lavapit = [mkplat(170, 400, 1, 8), mkplat(290, 400, 1, 8), mkplat(170, 540, 7, 1),\
           mkplat(190, 410, 5, 6.5, img=kbimg, deadly=True)]
elev1   = [mkosc((90,540), (90,400), 4, 1, 1.5)]
floors2 = [mkplat(40, 220, 15, 1), mkplat(380, 220, 17, 1),\
           mkplat(0, 260, 36, 1), mkplat(700, 240, 1, 1)]
circler = [mkcircler((480,380), 100, 3, 1, 60*5, 0, False)]
elev2   = [mkosc((720,450), (720, 220), 3, 1, 2)]
barrier = [mkplat(660, 180, 1, 2)]
stream  = [mkplat(100,180,2,1), mkplat(100, 200, 2, 1, img=kbimg, deadly=True),\
           mkplat(80,0,1,11, img=kbimg, deadly=True), mkplat(60,0,1,11),\
           mkplat(100,0,1,9)]
annoy   = [mkplat(480,20,1,8), mkplat(540,20,1,8), mkplat(600,20,1,8)]
blocker = [mkplat(180,180,12,1)]
cp1     = [mkcheckpoint(690,200)]
stair   = [mkplat(40,200,1,1), mkplat(20,120,1,1), mkplat(40,50,1,1)]
fin     = [mkfinish(40,30)]
obsts   = border + vborder + lavapit + elev1 + floors2 + circler + elev2 +\
          barrier + stream + blocker + annoy + cp1 + stair + fin

# ticks
proj    = [mkshooter((120,200), 1, 1, [5,0], 60, 104, kbimg, True)]
ticks   = proj


# TODO: this should probably just be a class or something
level = Level((20,560))
for obst in obsts:
    level.add_obst(obst)
for tick in ticks:
    level.add_tick(tick)
