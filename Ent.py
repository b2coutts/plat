#!/usr/bin/env python2

import pygame
from params import *
from util import *
import audio

class Ent:
    # xpos, ypos  # top-left corner position; floats, round to pixels
    # width, height
    # sprite
    # speed
    # grounded
    # behaviour
    # deadly, solid
    # level, level_idx
    # killsfx
    # spec

    def __init__(self, x, y, w, h, s=False, spd=[0,0], grd=False, beh=False,\
                       deadly=False, solid=True, killsfx=audio.sfx_died):
        self.xpos       = x
        self.ypos       = y
        self.oldx       = None
        self.oldy       = None
        self.width      = w
        self.height     = h
        self.sprite     = s
        self.speed      = spd[:]
        self.grounded   = grd
        self.behaviour  = beh
        self.jumping    = False
        self.deadly     = deadly
        self.solid      = solid
        self.level      = False
        self.level_idx  = False
        self.killsfx    = killsfx
        self.spec       = {}
        self.has_dash   = False
        self.has_blink  = False
        self.dashing    = False

    def __str__(self):
        pkeys = "xpos", "ypos", "width", "height", "speed",\
                "grounded", "deadly", "solid", "level_idx"
        return 'Ent: ' + ', '.join([k + "=" + str(self.__dict__[k])
                                    for k in pkeys if k in self.__dict__])

        return "Ent:  pos=(%s,%s),  size=%sx%s,  speed=%s, grounded=%s" %\
               (self.xpos, self.ypos, self.width, self.height, self.speed,\
                self.grounded)

    def unblit(self, screen, unblitted_rects):
        '''unblit self (in position from last frame), append to dirty_rects'''
        if self.sprite and self.oldx != None and\
           (self.oldx,self.oldy) != (round(self.xpos),round(self.ypos)):
            unimg = pygame.Surface((self.width, self.height))
            unimg.fill((0,0,0))
            screen.blit(unimg, (self.oldx,self.oldy))
            unblitted_rects.append((self.oldx, self.oldy, self.oldx+self.width,\
                                    self.oldy+self.height))

    def blitto(self, screen, unblitted_rects, dirty_rects):
        '''blit self to screen; append dirty rects to dirty_rects'''
        curx = round(self.xpos)
        cury = round(self.ypos)
        if self.sprite and ((self.oldx,self.oldy) != (curx,cury) or\
                            self.get_rect().collidelist(unblitted_rects) != -1):
            sprite = self.sprite(self) if hasattr(self.sprite, '__call__')\
                     else self.sprite
            if self.oldx == None:
                self.oldx = curx
                self.oldy = cury
            drx1 = min(curx, self.oldx)
            drx2 = max(curx, self.oldx) + self.width
            dry1 = min(cury, self.oldy)
            dry2 = max(cury, self.oldy) + self.height
            dirty_rects.append((drx1, dry1, drx2-drx1, dry2-dry1))
            screen.blit(sprite, (curx, cury))
            self.oldx = curx
            self.oldy = cury

    def get_rect(self):
        '''Gets the DRAW rect for self (rounded, not actual coords)'''
        return pygame.Rect(round(self.xpos), round(self.ypos), self.width,\
                           self.height)

    def centre(self):
        return [self.xpos + 0.5*self.width, self.ypos + 0.5*self.height]

    def left(self):
        return self.xpos

    def right(self):
        return self.xpos + self.width

    def top(self):
        return self.ypos

    def bottom(self):
        return self.ypos + self.height

    def pspeed(self):
        '''User speed after factoring in platform speed (if any)'''
        return vadd(self.speed, self.grounded.speed if self.grounded else [0,0])

    def kill(self, sfx = audio.sfx_died):
        self.xpos, self.ypos = self.level.spawn
        self.speed = [0,0]
        self.grounded = False
        audio.play(sfx)
