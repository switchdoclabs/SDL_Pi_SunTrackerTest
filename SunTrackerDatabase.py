#
# gathers data and writes to database
#
#

import MySQLdb as mdb

import Image
import ImageDraw
import ImageFont
import datetime

#    /*---------------------------------------------------------------------*/

TCA9545_CONFIG_BUS0  =                (0x01)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS1  =                (0x02)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS2  =                (0x04)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS3  =                (0x08)  # 1 = enable, 0 = disable

#/*=========================================================================*/


GAIN = 2/3

def writeDataToDatabase(currentSteps, currentDegrees,  disp, i2cMux, adc, SunAirPlus0, SunAirPlus1):



	#disp.clear()
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
		



	# turn on bus 1
        i2cMux.write_control_register(TCA9545_CONFIG_BUS1)
	# the three channels of the INA3221 named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
	LIPO_BATTERY_CHANNEL = 1
	SOLAR_CELL_CHANNEL   = 2
	OUTPUT_CHANNEL       = 3

	# Write two lines of text.
        nowPST = datetime.datetime.now() - datetime.timedelta(seconds=7*60*60);

        print "two step at currentTime PST = %s" % nowPST.strftime("%Y-%m-%d %H:%M:%S");
	draw.text((x, top),    '%s' % (nowPST.strftime("%Y-%m-%d %H:%M:%S")),  font=font, fill=255)
	draw.text((x, top+10),    '---------------',  font=font, fill=255)

	# gather data from SunAirPlus
	print "gathering data";

        print "-----------SunAirPlus 0--------------"
        shuntvoltage1 = 0
        busvoltage1   = 0
        current_mA1   = 0
        loadvoltage1  = 0


        busvoltage1 = SunAirPlus0.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
        shuntvoltage1 = SunAirPlus0.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
        # minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
        current_mA1 = SunAirPlus0.getCurrent_mA(LIPO_BATTERY_CHANNEL)

        loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)

        print "LIPO_Battery Bus Voltage: %3.2f V " % busvoltage1
        print "LIPO_Battery Load Voltage:  %3.2f V" % loadvoltage1
        print "LIPO_Battery Current 1:  %3.2f mA" % current_mA1
        print

        shuntvoltage2 = 0
        busvoltage2 = 0
        current_mA2 = 0
        loadvoltage2 = 0

        busvoltage2 = SunAirPlus0.getBusVoltage_V(SOLAR_CELL_CHANNEL)
        current_mA2 = -SunAirPlus0.getCurrent_mA(SOLAR_CELL_CHANNEL)
        loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)

        print "Solar Cell Bus Voltage 2:  %3.2f V " % busvoltage2
        print "Solar Cell Load Voltage 2:  %3.2f V" % loadvoltage2
        print "Solar Cell Current 2:  %3.2f mA" % current_mA2
        print

        shuntvoltage3 = 0
        busvoltage3 = 0
        current_mA3 = 0
        loadvoltage3 = 0

        busvoltage3 = SunAirPlus0.getBusVoltage_V(OUTPUT_CHANNEL)
        current_mA3 = SunAirPlus0.getCurrent_mA(OUTPUT_CHANNEL)
        loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)

        print "Output Bus Voltage 3:  %3.2f V " % busvoltage3
        print "Output Load Voltage 3:  %3.2f V" % loadvoltage3
        print "Output Current 3:  %3.2f mA" % current_mA3
        print

	# Write two lines of text.
	draw.text((x, top+20),    'STS=%3.1fV %3.1fmA' % (busvoltage2,current_mA2),  font=font, fill=255)
	draw.text((x, top+30),    'STB=%3.1fV %3.1fmA' % (busvoltage1,current_mA1),  font=font, fill=255)

        i2cMux.write_control_register(TCA9545_CONFIG_BUS3)

	# read in the solar panel voltage

	#resistor_voltage0 = adc.read_adc(0, gain=GAIN)*0.0001875
	#resistor_current0 = resistor_voltage0/10.0; 
  	#power_delivered0 = resistor_voltage0 * resistor_current0;
	#print "Resistor_voltage0 = %5.3fV Resistor_current0_mA = %5.3fmA Power_Delivered=%5.3fW" % (resistor_voltage0 , resistor_current0*1000, power_delivered0);

	# Put record in MySQL

	print "writing data 0";

	# open database
        con = mdb.connect('localhost', 'root', 'password', 'SunTracker');

        # you must create a Cursor object. It will let
        # you execute all the queries you need
        cur = con.cursor()

	# write record
	deviceid = 0
        query = 'INSERT INTO SolarPowerData(timestamp, deviceid, currentSteps, currentDegrees, battery_load_voltage, battery_current, solarcell_load_voltage, solarcell_current, output_load_voltage, output_current) VALUES(UTC_TIMESTAMP(), %i, %i, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  currentSteps, currentDegrees, busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3)
        print("query=%s" % query)

        cur.execute(query)
	

	# now fetch other data and save
        i2cMux.write_control_register(TCA9545_CONFIG_BUS2)

	# gather data from SunAirPlus
	print "gathering data";

        print "-----------SunAirPlus 1--------------"
        shuntvoltage1 = 0
        busvoltage1   = 0
        current_mA1   = 0
        loadvoltage1  = 0


        busvoltage1 = SunAirPlus0.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
        shuntvoltage1 = SunAirPlus0.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
        # minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
        current_mA1 = SunAirPlus0.getCurrent_mA(LIPO_BATTERY_CHANNEL)

        loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)

        print "LIPO_Battery Bus Voltage: %3.2f V " % busvoltage1
        print "LIPO_Battery Load Voltage:  %3.2f V" % loadvoltage1
        print "LIPO_Battery Current 1:  %3.2f mA" % current_mA1
        print

        shuntvoltage2 = 0
        busvoltage2 = 0
        current_mA2 = 0
        loadvoltage2 = 0

        busvoltage2 = SunAirPlus0.getBusVoltage_V(SOLAR_CELL_CHANNEL)
        current_mA2 = -SunAirPlus0.getCurrent_mA(SOLAR_CELL_CHANNEL)
        loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)

        print "Solar Cell Bus Voltage 2:  %3.2f V " % busvoltage2
        print "Solar Cell Load Voltage 2:  %3.2f V" % loadvoltage2
        print "Solar Cell Current 2:  %3.2f mA" % current_mA2
        print

        shuntvoltage3 = 0
        busvoltage3 = 0
        current_mA3 = 0
        loadvoltage3 = 0

        busvoltage3 = SunAirPlus0.getBusVoltage_V(OUTPUT_CHANNEL)
        current_mA3 = SunAirPlus0.getCurrent_mA(OUTPUT_CHANNEL)
        loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)

        print "Output Bus Voltage 3:  %3.2f V " % busvoltage3
        print "Output Load Voltage 3:  %3.2f V" % loadvoltage3
        print "Output Current 3:  %3.2f mA" % current_mA3
        print


        i2cMux.write_control_register(TCA9545_CONFIG_BUS3)

	# read in the solar panel voltage

	#resistor_voltage1 = adc.read_adc(1, gain=GAIN)*0.0001875
	#resistor_current1 = resistor_voltage1/10.0; 
  	#power_delivered1 = resistor_voltage1 * resistor_current0;
	#print "Resistor_voltage1 = %5.3fV Resistor_current1_mA = %5.3fmA Power_Delivered=%5.3fW" % (resistor_voltage1 , resistor_current1*1000, power_delivered1);

	# Put record in MySQL

	print "writing data 1";

	# write record
	deviceid = 1
        query = 'INSERT INTO SolarPowerData(timestamp, deviceid, currentSteps, currentDegrees, battery_load_voltage, battery_current, solarcell_load_voltage, solarcell_current, output_load_voltage, output_current) VALUES(UTC_TIMESTAMP(), %i, %i, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  currentSteps, currentDegrees, busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3)
        print("query=%s" % query)

        cur.execute(query)
	
	# Write two lines of text.
	draw.text((x, top+40),    'FXS=%3.1fV %3.1fmA' % (busvoltage2,current_mA2),  font=font, fill=255)
	draw.text((x, top+50),    'FXB=%3.1fV %3.1fmA' % (busvoltage1,current_mA1),  font=font, fill=255)



	
	
	# Display image.
	disp.image(image)
	disp.display()

	
	# close database
        
        con.commit()    
        i2cMux.write_control_register(TCA9545_CONFIG_BUS0)

	return




