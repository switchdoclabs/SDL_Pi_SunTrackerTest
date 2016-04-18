#!/usr/bin/env python
#
#
#    Grove Mini I2C Motor Driver - Raspberry Pi
#
#
#    SwitchDoc Labs March 2016
#    Version 1.0
#


from time import sleep
import smbus

# constants

#/*=========================================================================
#    I2C ADDRESS/BITS
#    -----------------------------------------------------------------------*/
MOTORA_DRV8830 =                         (0x62)   # Channel 1
MOTORB_DRV8830 =                         (0x60)   # Channel 2
#/*=========================================================================*/

#/*=========================================================================
#    CONFIG REGISTER (R/W)
#    -----------------------------------------------------------------------*/

#    /*---------------------------------------------------------------------*/

# Fault constants
DRV8830_FAULT 	 = (0x01)
DRV8830_ILIMIT   = (0x10)
DRV8830_OTS      = (0x08)
DRV8830_UVLO     = (0x04)
DRV8830_OCP      = (0x02)
#/*=========================================================================*/


class SDL_Pi_GROVE_DRV8830():


    	def __init__(self, twi=1 ):
        	self._bus = smbus.SMBus(twi)


	def returnMotorAddress(self,motorNumber):

		if (motorNumber == 0):
			return MOTORA_DRV8830
		else:
			return MOTORB_DRV8830

	# Return the fault status of the DRV8830 chip. Also clears any existing faults.
	def getFault(self, motorNumber):
 
		motorAddress = self.returnMotorAddress(motorNumber) 
		buffer = 0
  
		clearFault = 0x80
  
		buffer = self.wireReadRegister(motorAddress,0x01)

		self.wireWriteRegister(motorAddress, 0x01, clearFault)
		return buffer;

	def drive(self, motorNumber,speed):
		
		motorAddress = self.returnMotorAddress(motorNumber) 

		# first clear any fault
		clearFault = 0x80
		self.wireWriteRegister(motorAddress, 0x01, clearFault)
		
		regValue = abs(speed)      # Find the byte-ish abs value of the input
  		if (regValue > 63):
			regValue = 63; # Cap the value at 63.
  			regValue = regValue<<2           # Left shift to make room for bits 1:0
  		if (speed < 0):
			regValue |= 0x01  # Set bits 1:0 based on sign of input.
  		else:           
			regValue |= 0x02
  
  		self.wireWriteRegister(motorAddress, 0x00, regValue)  	

		return

	def stop(self, motorNumber):
		
		motorAddress = self.returnMotorAddress(motorNumber) 
		self.wireWriteRegister(motorAddress, 0x00, 0)
		return

	def brake(self, motorNumber):
		motorAddress = self.returnMotorAddress(motorNumber) 
		self.wireWriteRegister(motorAddress, 0x00, 0x03)
		return


 	def wireWriteRegister(self, motorAddress, reg, value):

        	#print "addr =0x%x register = 0x%x data = 0x%x " % (motorAddress, reg, value)
		self._bus.write_byte_data(motorAddress, reg, value)

    
	def wireReadRegister(self, motorAddress, reg ):

		returndata = self._bus.read_byte_data(motorAddress, reg)
        	#print "addr = 0x%x data = 0x%x %i returndata = 0x%x " % (motorAddress, reg, reg, returndata)
        	return returndata
