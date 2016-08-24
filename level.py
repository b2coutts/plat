#!/usr/bin/env python2

from Ent import *
import params

bwidth = 20
w,h = params.SCREEN_SIZE

blockimg = pygame.image.load("img/block.png")

def mover_beh(plat, frame):
    if (frame+1)%(60*5) == 0:
        plat.speed[0] *= -1

def elev_beh(plat, frame):
    if (frame+1)%(60*7) == 0:
        plat.speed[1] *= -1

b_top   = Ent(-bwidth, -bwidth, w + 2*bwidth, bwidth)
b_left  = Ent(-bwidth, -bwidth, bwidth, h + 2*bwidth)
b_right = Ent(w, -bwidth, bwidth, h + 2*bwidth)
b_bot   = Ent(-bwidth, h, w + 2*bwidth, bwidth)
plat1   = Ent(200, 340, 20, 20, blockimg)
plat2   = Ent(220, 340, 20, 20, blockimg)
movers  = [Ent(200+x, 300, 20, 20, blockimg, [1,0], beh=mover_beh)\
           for x in [0,20,40,60,80] ]
elevator = [Ent(50+x, 350, 20, 20, blockimg, [0,-1], beh=elev_beh)\
            for x in [0,20,40,60,80]]

# TODO: this should probably just be a class or something
level = [b_top, b_left, b_right, b_bot, plat1, plat2] + movers + elevator
