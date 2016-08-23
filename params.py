#!/usr/bin/env python2

SCREEN_SIZE             = 600, 400

# highest distance that counts as a collision
COLL_DIST               = 0.5

# amount of separation in collision resolution; should be >COLL_DIST
COLL_SEP                = 0.55

FRAME_LENGTH            = 0.0167
#FRAME_LENGTH           = 0.167
RUN_SPEED               = 3.5
AIR_SPEED               = 3.5
JUMP_SPEED              = 10.0

AIR_ACCEL               = 0.3
FRIC_DECEL              = 0.1
FRIC_DECEL_SLOW         = 0.00
FRIC_DECEL_SLOW_THRES   = 0.75
GRAV_ACCEL              = 0.5
