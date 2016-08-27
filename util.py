#!/usr/bin/env python2

import math
from params import *

def vadd(a,b):
    '''Add two vectors a and b'''
    return [c+d for c,d in zip(a,b)]

def vsub(a,b):
    '''Subtract two vectors a and b'''
    return [c-d for c,d in zip(a,b)]

def vscale(k,v):
    '''Scale a vector v by scalar k'''
    return [k*x for x in v]

def vdot(a,b):
    '''Dot product'''
    return sum([c*d for c,d in zip(a,b)])

def vperp2(v):
    '''Perpendicular vector to v; 2-dim only'''
    return [-v[1], v[0]]

def vnorm(v):
    '''2-norm'''
    return math.sqrt(vdot(v,v))

def rotccw(v, theta):
    '''rotate 2D vector v counter-clockwise by theta'''
    return [math.cos(theta)*v[0] - math.sin(theta)*v[1],
            math.sin(theta)*v[0] + math.cos(theta)*v[1]]

def amin(a,b):
    '''Produces whichever of a,b has lesser absolute value'''
    return a if abs(a) < abs(b) else b

def absfloor(x):
    '''Produces the integer nearest to x which has lesser absolute value'''
    return (x/abs(x)) * floor(abs(x))

def rect_coll(r1,r2,epsilon):
    '''Determine if two rects (x,y,w,h) come witin epsilon of intersecting'''
    return r1[0] < r2[0] + r2[2] + epsilon and\
           r1[1] < r2[1] + r2[3] + epsilon and\
           r2[0] < r1[0] + r1[2] + epsilon and\
           r2[1] < r1[1] + r1[3] + epsilon

def float_eq(a,b):
    return abs(a-b) < EPSILON
