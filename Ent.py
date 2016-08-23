#!/usr/bin/env python2

import pygame

class Ent:
    #xpos, ypos  # top-left corner position; floats, round to pixels
    #width, height
    #sprite
    #speed
    #grounded

    def __init__(self, x, y, w, h, s = False, speed = [0,0], grounded = False):
        self.xpos = x
        self.ypos = y
        self.width = w
        self.height = h
        self.sprite = s
        self.speed = speed
        self.grounded = grounded

    def blitto(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (round(self.xpos), round(self.ypos)))

    def get_rect(self):
        return self.xpos, self.ypos, self.width, self.height

    def display(self):
        print "pos: (%s,%s),  size: %sx%s,  speed: %s, grounded: %s" %\
              (self.xpos, self.ypos, self.width, self.height, self.speed,\
               self.grounded)

    def centre(self):
        return [self.xpos + 0.5*self.width, self.ypos + 0.5*self.height]
