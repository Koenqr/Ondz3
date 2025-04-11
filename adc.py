#Raspberry pi pico2 ADC readout

import time
import machine

class ADC:
	def __init__(self, pin):
		self.ADC = machine.ADC(pin)
  
	def read(self):
		reading = self.ADC.read_u16()
		return reading, reading * 3.3 / 65535

	def multiSample(self, n):
		samples = []
		for i in range(n):
			samples.append(self.read())
			time.sleep(0.001)
		mean = sum([x[1] for x in samples])/n
		stdev = (sum([(x[1]-mean)**2 for x in samples])/n)**0.5
		return mean, stdev
		
		

if __name__ == "__main__":
	import utime
	adc = ADC(28)
	while True:
		print(adc.read())
		utime.sleep(1)