#!/usr/bin/env python
#
#
#  SunTracking Test Software
# Rasbperry Pi
#
# SwitchDoc Labs, April 2016
#

# imports

import sys

import sys
sys.path.append('./SDL_Pi_INA3221')
sys.path.append('./Adafruit_Python_ADS1x15')

import time
import datetime
import random 
import SDL_Pi_GROVE_DRV8830 

import SunTrackerDatabase
import SDL_Pi_TCA9545
import SDL_Pi_GROVE_Stepper

import SDL_Pi_INA3221

# Import the ADS1x15 module.
import Adafruit_ADS1x15

#create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()


#import Adafruit
import subprocess


import Adafruit_SSD1306


import Image
import ImageDraw
import ImageFont

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24, i2c_address=0x3C)

disp.begin()

disp.clear()
disp.display()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)


# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8)

# Load default font.
font = ImageFont.load_default()

x=0
top = 2

# Write two lines of text.
draw.text((x, top),    'SunTracker',  font=font, fill=255)
draw.text((x, top+10), 'SwitchDoc Labs!', font=font, fill=255)

# Display image.
disp.image(image)
disp.display()

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

# set up I2C Mux card for translateion to 5V for the motors and the two SunAirPlus boards

i2cMux = SDL_Pi_TCA9545.SDL_Pi_TCA9545(addr=TCA9545_ADDRESS, bus_enable = TCA9545_CONFIG_BUS0)



# turn on bus 1
i2cMux.write_control_register(TCA9545_CONFIG_BUS1)
SunAirPlus0 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)
# turn on bus 2
i2cMux.write_control_register(TCA9545_CONFIG_BUS2)
SunAirPlus1 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)
# turn on bus 0
i2cMux.write_control_register(TCA9545_CONFIG_BUS0)


print ""
print "SunTracker Version 1.0 - SwitchDoc Labs"
print "March 2016"
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""


i2ccommand = "sudo i2cdetect -y 1"
output = subprocess.check_output (i2ccommand,shell=True, stderr=subprocess.STDOUT )
print output

print "-----------------------------------"
print

# turn on bus 0
i2cMux.write_control_register(TCA9545_CONFIG_BUS0)
groveMini = SDL_Pi_GROVE_DRV8830.SDL_Pi_GROVE_DRV8830()

stepper = SDL_Pi_GROVE_Stepper.SDL_Pi_GROVE_Stepper(groveMini,513)

stepper.setSpeed(25, 25)

print "fault Motor 0 %i" % (groveMini.getFault(0))

print "fault Motor 1 %i" % (groveMini.getFault(1))

# we go 180 degrees from Due East to Due West 
# As of March 29, Sun rises at SwtichDoc Labs at 06:32 and sets at 19:15 for 12:43 minutes of Sun
# so we do the calcuations based upon 763 minutes of Sun.   That is 0.236 degrees per minute.
# based on the stepper motor we are using (513 for 360 degrees) We get 0.70 degree per step.
# this means we should do 1 step every three minutes or two steps every six minutes.

# calculate where the sun is depending on the time we start....
# set sunrise
sunriseTimeUTC = datetime.datetime.now();
sunriseTimeUTC = sunriseTimeUTC.replace(hour=6, minute=38)+datetime.timedelta(seconds=7*60*60);  #UTC 7 hours ahead 



print "sunriseTime UTC = %s" % (sunriseTimeUTC.strftime("%Y-%m-%d %H:%M:%S"));
sunriseTimePST = sunriseTimeUTC - datetime.timedelta(seconds=7*60*60);
print "sunriseTime PST = %s" % sunriseTimePST.strftime("%Y-%m-%d %H:%M:%S");

# assume we start the day Due East.

# calculate where we should be pointing at this time.

minutesAfterSunriseDT = datetime.datetime.now() - sunriseTimeUTC ;
minutesAfterSunrise = minutesAfterSunriseDT.seconds/60;
while (minutesAfterSunrise < 0):
	# still dark
	delay(60.0)
	minutesAfterSunriseDT = datetime.datetime.now() - sunriseTimeUTC ;
	minutesAfterSunrise = minutesAfterSunriseDT.seconds/60;
	print "minutes before sunrise = %i" % (-minutesAfterSunrise);

print "minutes after sunrise = %i" % (minutesAfterSunrise);


initialSteps = minutesAfterSunrise * 0.236/0.70;
print "initialSteps = %i" % (initialSteps);

# Poll timing 

stepper.step(initialSteps);

currentSteps = initialSteps;
currentDegrees = currentSteps * 0.7
numberOfMinutesLeftInDay = 751 - minutesAfterSunrise;

for x in range (0, numberOfMinutesLeftInDay):

	if ((x % 6) == 0):
		# advance two steps every 6 minutes 
		nowPST = datetime.datetime.now() - datetime.timedelta(seconds=7*60*60);

		print "two step at currentTime PST = %s" % nowPST.strftime("%Y-%m-%d %H:%M:%S");
		stepper.step(2)
		currentSteps = currentSteps + 2
		currentDegrees = currentSteps * 0.7

	
	# every minute, take samples
	print "Data saved:"+ time.strftime("%Y-%m-%d %H:%M:%S")

	SunTrackerDatabase.writeDataToDatabase(currentSteps, currentDegrees, disp, i2cMux, adc, SunAirPlus0, SunAirPlus1);
 	#time.sleep(1.0);	# delay 1 seconds
 	time.sleep(60);	# delay 60 seconds

# reset for tomorrow

stepper.step(-256)	
	
	
