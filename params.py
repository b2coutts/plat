#!/usr/bin/env python2

# debug constants
# enables debug-only features
DEBUG                   = True
# 0 for speed boosts, 1 for gun
MOUSE_MODE              = 1

SCREEN_SIZE             = 800, 600
#SCREEN_SIZE             = 1280, 800

# amount of distance maintained between user and obstacles
COLL_BUFFER             = 0.5

FRAME_LENGTH            = 0.0167
#FRAME_LENGTH           = 0.167
RUN_SPEED               = 3.5
AIR_SPEED               = 3.5
JUMP_ACCEL              = 1.7
JUMP_ACCEL_LEN          = 5

DASH_SPEED              = 10.0
DASH_DECEL              = 0.3
DASH_DURATION           = 5

BLINK_DIST              = 80
BLINK_COOLDOWN          = 60

AIR_ACCEL               = 0.3
FRIC_DECEL              = 0.1
FRIC_DECEL_SLOW         = 0.00
FRIC_DECEL_SLOW_THRES   = 0.75
GRAV_ACCEL              = 0.5
GRAV_ACCEL_RAT_MIN      = 0.5
GRAV_ACCEL_RAT_COEF     = (GRAV_ACCEL_RAT_MIN-1) / (JUMP_ACCEL*JUMP_ACCEL_LEN)

BOOST_SPEED             = 8.0

BULLET_SPEED            = 10.0
GUN_COOLDOWN            = 40

# common buffer to consider 2 floats 'equal'
EPSILON                 = 0.001
