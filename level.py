#!/usr/bin/env python2

from Ent import *
import params

bwidth = 20
w,h = params.SCREEN_SIZE

blockimg = pygame.image.load("img/block.png")

b_top   = Ent(-bwidth, -bwidth, w + 2*bwidth, bwidth)
b_left  = Ent(-bwidth, -bwidth, bwidth, h + 2*bwidth)
b_right = Ent(w, -bwidth, bwidth, h + 2*bwidth)
b_bot   = Ent(-bwidth, h, w + 2*bwidth, bwidth)
plat1   = Ent(200, 340, 20, 20, blockimg)
plat2   = Ent(220, 340, 20, 20, blockimg)

# TODO: this should probably just be a class or something
level = [b_top, b_left, b_right, b_bot, plat1, plat2]
lvl_rects = [b.get_rect() for b in level]
