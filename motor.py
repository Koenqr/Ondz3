#motor lib for 28byj-48 stepper motor with uln2003 driver




import machine
import utime


class StepperMotor:
	commutation_table = [
		[1,1,0,0],
		[0,1,1,0],
		[0,0,1,1],
		[1,0,0,1]
	]
	index=0
	
	def __init__(self, pin1, pin2, pin3, pin4):
		self.pins = [machine.Pin(pin1, machine.Pin.OUT), machine.Pin(pin2, machine.Pin.OUT), machine.Pin(pin3, machine.Pin.OUT), machine.Pin(pin4, machine.Pin.OUT)]
		self.index = 0
	
	def step(self, direction):
		if direction == 1:
			self.index = (self.index + 1) % 4
		else:
			self.index = (self.index - 1) % 4
		for i in range(4):
			self.pins[i].value(self.commutation_table[self.index][i])
   
   
if __name__ == "__main__":
	motor = StepperMotor(0, 1, 2, 3)
	while True:
		motor.step(0)
		print(motor.index)
		utime.sleep(0.05)
		