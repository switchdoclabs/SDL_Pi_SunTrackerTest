#!/usr/bin/env python

# modified by SwitchDoc Labs for the Grove DRV8330 Stepper motor

# roughly based on Hercules_Stepper.cpp Seeed Technology

from time import sleep

class SDL_Pi_GROVE_Stepper():



    	def __init__(self, GroveDRV8830, number_of_steps ):
        	self._GroveDRV8830 = GroveDRV8830
		self.SPD_BUFF_STEPS = 100
  		self.step_number = 0      # which step the motor is on
    		self.direction   = 0      # motor direction
    		self.number_of_steps = number_of_steps;    # total number of steps for this motor


    		# pin_count is used by the stepMotor() method:
    		self.pin_count = 4;


	# Sets the speed in revs per minute

	def setSpeed(self, rpm_start, rpm_max):

	        self.delay_max_speed = 60 * 1000 *1000 / self.number_of_steps / rpm_max;
    		self.delay_start_speed = 60 * 1000 * 1000/ self.number_of_steps / rpm_start;
		return


	# Moves the motor steps_to_move steps.  If the number is negative,
   	# the motor moves in the reverse direction.


	def step(self, steps_to_move):


	    	steps_left = abs(steps_to_move)  # how many steps to take
    		steps_orig = steps_left
    		steps_buffer = self.SPD_BUFF_STEPS

    		if (steps_orig < steps_buffer*2):
	
    			steps_buffer = steps_left/2;

    		delays = self.delay_start_speed;
    		delay_minus = (delays - self.delay_max_speed)/self.SPD_BUFF_STEPS;

    		# determine direction based on whether steps_to_mode is + or -:
    		if (steps_to_move > 0):
			 self.direction = 1
    		if (steps_to_move < 0):
			 self.direction = 0

    	 	# decrement the number of steps, moving one step each time:
    		while(steps_left > 0): 
        		sleep(delays/1000000.0) # in microseconds
        		if (self.direction == 1):
            			self.step_number = self.step_number+1
            			if (self.step_number == self.number_of_steps): 
                			self.step_number = 0;
        
       			else: 
            			if (self.step_number == 0):
                			self.step_number = self.number_of_steps;
            			self.step_number= self.step_number -1
        
       			# decrement the steps left:
        		steps_left = steps_left-1;
        		if ((steps_orig - steps_left) <= steps_buffer):
        			delays = delays - delay_minus
        		else:  
				if (steps_left <= steps_buffer):
        				delays = delays+delay_minus

        		# step the motor to step number 0, 1, 2, or 3:
        		self.stepMotor(self.step_number % 4);



	# Moves the motor forward or backwards.
 
	def stepMotor(self, thisStep):

    		if (self.pin_count == 4): 
        		
             		if (thisStep == 0):    # 1010
            
				self._GroveDRV8830.drive(0, 100);
            			self._GroveDRV8830.drive(1, 100);
           			return 
            
            		if (thisStep ==  1):    # 0110
            			self._GroveDRV8830.drive(0,-100);
            			self._GroveDRV8830.drive(1, 100);
           			return 
            		if (thisStep == 2):     # 0101
            
            			self._GroveDRV8830.drive(0,-100);
            			self._GroveDRV8830.drive(1,-100);
           			return 
            		if (thisStep == 3):     # 1001
            
            			self._GroveDRV8830.drive(0, 100);
            			self._GroveDRV8830.drive(1,-100);
           			return 

            		self._GroveDRV8830.drive(0);
            		self._GroveDRV8830.drive(0);
