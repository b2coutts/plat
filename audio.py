#!/usr/bin/env python2

import pygame

bgm = pygame.mixer.Sound("audio/bgm1.flac")

# sound effects
sfx_jump = pygame.mixer.Sound("audio/jump.wav")
sfx_died = pygame.mixer.Sound("audio/died.wav")
sfx_fire = pygame.mixer.Sound("audio/fire.wav")
sfx_cp   = pygame.mixer.Sound("audio/cp.wav")
sfx_water= pygame.mixer.Sound("audio/water.wav")
sfx_dash = pygame.mixer.Sound("audio/dash.wav")
sfx_blink= pygame.mixer.Sound("audio/blink.wav")

def init():
    pygame.mixer.init()
    bgm.play(loops=-1)

def play(sfx):
    sfx.play()
