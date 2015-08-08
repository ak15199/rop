#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import random
import signal
import sys


def signal_handler(signal, frame):
	print("SIGINT caught, exiting gracefully.")
	shutdown()

def shutdown(quit=True):
	for hat in hats:
		hat.shutdown()
	if quit:
		sys.exit(0)

class Hat(object):
	def __init__(self, addr, motorlist, verbose=False):
		self.name = addr
		self.verbose = verbose
		self.hat = Adafruit_MotorHAT(int(addr, 16))
		self.motors = dict([(m, self.hat.getMotor(m)) for m in motorlist])
		self.until = dict([(m, None) for m in motorlist])
		self.init_motors()

	def init_motors(self):
		for motorname, motor in self.motors.items():
			motor.setSpeed(150)
			motor.run(Adafruit_MotorHAT.FORWARD)
			motor.run(Adafruit_MotorHAT.RELEASE)
			if self.verbose:
				print("init hat %s motor %s" % (self.name, motorname))

	def shutdown(self):
		for motorname, motor in self.motors.items():
			self.until[motorname] = None
			motor.run(Adafruit_MotorHAT.RELEASE)
			if self.verbose:
				print("shutdown hat %s motor %s" % (self.name, motorname))

	def run(self, motorname, direction, speedpct, text=""):
		if speedpct < 1:
			self.motors[motorname].run(Adafruit_MotorHAT.RELEASE)
			if self.verbose:
				print("hat %s motor %s resting %s" % (self.name, motorname, text))
		else:
			direction = Adafruit_MotorHAT.FORWARD if direction[0].upper() == "F" else Adafruit_MotorHAT.BACKWARD
			speed = int((speedpct if speedpct < 1.0 else speedpct / 100.0) * 253)
			self.motors[motorname].run(direction)
			self.motors[motorname].setSpeed(speed)
			if self.verbose:
				print("hat %s motor %s running %s at speed %s %s" %
						(self.name, motorname, direction, speed, text))

	def run_for(self, motorname, direction, speedpct, runtime=10):
		self.until[motorname] = time.time() + runtime
		self.run(motorname, direction, speedpct, text="for %ss" % int(runtime))

	def run_random(self, motorname):
		direction = "F" if random.getrandbits(1) == 0 else "B"
		speedpct = abs(int(random.gauss(40, 30)))
		runtime = abs(random.gauss(10, 3))
		speedpct = 0 if speedpct > 70 or runtime > 20 else speedpct
		self.run_for(motorname, direction, speedpct, runtime)

	def run_all_random(self):
		for motorname, motor in self.motors.items():
			self.run_random(motorname)

	def check_all_and_restart(self):
		for motorname, until in self.until.items():
			if until is None or time.time() > until:
				self.run_random(motorname)




if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)

	# h60 = Hat('0x60', [1,2,3,4], verbose=True)
	h66 = Hat('0x66', [1,2,3,4], verbose=True)
	# h67 = Hat('0x67', [1,2,3,4], verbose=True)
	hats = [h66]

	# h66.run_for(1, 'B', 5)
	# h60.run_for(2, 'B', 5)
	# h67.run_for(1, 'B', 5)
	# h67.run_for(2, 'B', 5)
	# h67.run_for(3, 'B', 5)
	# h67.run_for(4, 'B', 5)
	# time.sleep(10)

	# h66.run_for(1, 'F', 10)
	# h60.run_for(2, 'F', 10)
	# h67.run_for(1, 'F', 10)
	# h67.run_for(2, 'F', 10)
	# h67.run_for(3, 'F', 10)
	# h67.run_for(4, 'F', 10)
	# time.sleep(10)

	h66.run_for(1, 'B', 25)
	h66.run_for(2, 'B', 25)
	h66.run_for(3, 'B', 25)
	h66.run_for(4, 'B', 25)
	# h60.run_for(2, 'B', 25)
	# h67.run_for(1, 'B', 25)
	# h67.run_for(2, 'B', 25)
	# h67.run_for(3, 'B', 25)
	# h67.run_for(4, 'B', 25)
	# time.sleep(10)

	h66.run_for(1, 'F', 40)
	h66.run_for(2, 'F', 40)
	h66.run_for(3, 'F', 40)
	h66.run_for(4, 'F', 40)
	# h60.run_for(2, 'F', 40)
	# h67.run_for(1, 'F', 40)
	# h67.run_for(2, 'F', 40)
	# h67.run_for(3, 'F', 40)
	# h67.run_for(4, 'F', 40)
	time.sleep(10)

	h66.run_for(1, 'B', 50)
	h66.run_for(2, 'B', 50)
	h66.run_for(3, 'B', 50)
	h66.run_for(4, 'B', 50)
	# h60.run_for(2, 'B', 50)
	# h67.run_for(1, 'B', 50)
	# h67.run_for(2, 'B', 50)
	# h67.run_for(3, 'B', 50)
	# h67.run_for(4, 'B', 50)
	time.sleep(10)

	h66.run_for(1, 'B', 65)
	h66.run_for(2, 'B', 65)
	h66.run_for(3, 'B', 65)
	h66.run_for(4, 'B', 65)
	# h60.run_for(2, 'B', 65)
	# h67.run_for(1, 'B', 65)
	# h67.run_for(2, 'B', 65)
	# h67.run_for(3, 'B', 65)
	# h67.run_for(4, 'B', 65)
	time.sleep(10)


	shutdown()