import adc
import motor

import machine
import time

#OC 300MHz
machine.freq(300000000)



#open ADC on pin 28
adc = adc.ADC(28)
#open motor on pins 0,1,2,3
motor = motor.StepperMotor(0, 1, 2, 3) #angle per step is 5.625/64*(17/77) = 0.0194044237012987

for i in range(180):
	for z in range(int(100*(97/360))):
		motor.step(1)
		time.sleep(1/420)
  



print("START SERIES")

while True:
	#wait for keyboad interrupt
	
	#sweep 270 deg taking an ADC every 1 deg
	
	for i in range(180):
		for z in range(int(100*(97/360))):
			motor.step(0)
			time.sleep(1/360)
		time.sleep(0.25)
		reading=adc.multiSample(100)
		#str format "i;mean;stdev"
		print(f"{i};{reading[0]};{reading[1]}")
  
	_=input("END SERIES") #wait for keyboard interrupt
	
	