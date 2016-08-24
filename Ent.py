#!/usr/bin/env python2

import pygame
from params import *
from util import *

class Ent:
    #xpos, ypos  # top-left corner position; floats, round to pixels
    #width, height
    #sprite
    #speed
    #grounded
    #behaviour

    def __init__(self, x, y, w, h, s=False, spd=[0,0], grd=False, beh=False):
        self.xpos = x
        self.ypos = y
        self.width = w
        self.height = h
        self.sprite = s
        self.speed = spd[:]
        self.grounded = grd
        self.behaviour = beh
        self.jumping = False

    def __str__(self):
        return "Ent:  pos=(%s,%s),  size=%sx%s,  speed=%s, grounded=%s" %\
               (self.xpos, self.ypos, self.width, self.height, self.speed,\
                self.grounded)

    def blitto(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (round(self.xpos), round(self.ypos)))

    def get_rect(self):
        return self.xpos, self.ypos, self.width, self.height

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


    def kill(self):
        self.xpos, self.ypos = SPAWN
        self.speed = [0,0]
        self.grounded = False
