#!/usr/bin/env python
#
#
# Test case for Grove DRV8830
# SDL_Pi_GROVE_DRV8830 Library for Rasbperry Pi
#
# SwitchDoc Labs, March 2016
#

# imports

import sys
import time
import datetime
import random 
import SDL_Pi_GROVE_DRV8830 

import SDL_Pi_TCA9545
import SDL_Pi_GROVE_Stepper

import subprocess


#/*=========================================================================
#    I2C ADDRESS/BITS
#    -----------------------------------------------------------------------*/
TCA9545_ADDRESS =                         (0x73)    # 1110011 (A0+A1=VDD)
#/*=========================================================================*/

#/*=========================================================================
#    CONFIG REGISTER (R/W)
#    -----------------------------------------------------------------------*/
TCA9545_REG_CONFIG            =          (0x00)
#    /*---------------------------------------------------------------------*/

TCA9545_CONFIG_BUS0  =                (0x01)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS1  =                (0x02)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS2  =                (0x04)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS3  =                (0x08)  # 1 = enable, 0 = disable

#/*=========================================================================*/


print ""
print "Test SDL_Pi_GROVE_DVR8830 Version 1.0 - SwitchDoc Labs"
print ""
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

tca9545 = SDL_Pi_TCA9545.SDL_Pi_TCA9545(addr=TCA9545_ADDRESS, bus_enable = TCA9545_CONFIG_BUS0)

i2ccommand = "sudo i2cdetect -y 1"
output = subprocess.check_output (i2ccommand,shell=True, stderr=subprocess.STDOUT )
print output

print "-----------------------------------"
print

groveMini = SDL_Pi_GROVE_DRV8830.SDL_Pi_GROVE_DRV8830()

stepper = SDL_Pi_GROVE_Stepper.SDL_Pi_GROVE_Stepper(groveMini,513)

stepper.setSpeed(100, 100)

print "fault Motor 0 %i" % (groveMini.getFault(0))

print "fault Motor 1 %i" % (groveMini.getFault(1))


for x in range (0, 513):

	print "step  %i = " % x
	stepper.step(1)
	
