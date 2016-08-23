#!/usr/bin/env python2

def vadd(a,b):
    '''Add two vectors a and b'''
    return [c+d for c,d in zip(a,b)]

def vsub(a,b):
    '''Subtract two vectors a and b'''
    return [c-d for c,d in zip(a,b)]

def vdot(a,b):
    '''Dot product'''
    return sum([c*d for c,d in zip(a,b)])

def vperp2(v):
    '''Perpendicular vector to v; 2-dim only'''
    return [-v[1], v[0]]

def amin(a,b):
    '''Produces whichever of a,b has lesser absolute value'''
    return a if abs(a) < abs(b) else b

def absfloor(x):
    '''Produces the integer nearest to x which has lesser absolute value'''
    return (x/abs(x)) * floor(abs(x))

def rect_coll(r1,r2,epsilon):
    '''Determine if two rects (x,y,w,h) come witin epsilon of intersecting'''
    return r1[0] <= r2[0] + r2[2] + epsilon and\
           r1[1] <= r2[1] + r2[3] + epsilon and\
           r2[0] <= r1[0] + r1[2] + epsilon and\
           r2[1] <= r1[1] + r1[3] + epsilon

def cast(p, v, l):
    '''Given a starting point p, a direction v, and a line segment l (pair of
       endpoints), produce the positive number t such that p+tv is in l, or
       float('inf') if no such t exists'''
    d = vperp2(vsub(l[1],  l[0]))
    alpha = vdot(d,l[0])
    if vdot(d,v) == 0:
        return float('inf')
    t = (alpha - vdot(d,p)) / vdot(d,v)
    return t if t>=0 else float('inf')
