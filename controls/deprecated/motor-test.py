#!/usr/bin/python
#
# :Author: PB
# :Date: 4 Aug 2015
# :License: GPL v2
#
# motor tester for k Hats with a list of motors on each Hat


import time
import atexit
import random
import signal
import sys

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
sys.path.append("/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_ADS1x15")
import Adafruit_ADS1x15


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
		for motorname, motor in self.motors.items():
			motor.setSpeed(150)
			motor.run(Adafruit_MotorHAT.FORWARD)
			motor.run(Adafruit_MotorHAT.RELEASE)
			if self.verbose:
				print("init hat %s motor %s" % (self.name, motorname))

	def shutdown_one(self, motorname):
		self.until[motorname] = None
		motor = self.motors[motorname]
		motor.run(Adafruit_MotorHAT.RELEASE)
		if self.verbose:
			print("shutdown hat %s motor %s" % (self.name, motorname))

	def shutdown(self):
		for motorname, motor in self.motors.items():
			self.shutdown_one(motorname)

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
		speedpct = abs(int(random.gauss(60, 40)))
		runtime = abs(random.gauss(6, 3))
		speedpct = 0 if speedpct < 35 or runtime > 20 else speedpct
		self.run_for(motorname, direction, speedpct, runtime)

	def check_all_and_restart(self):
		for motorname, until in self.until.items():
			if until is None or time.time() > until:
				self.run_random(motorname)

	def test_on(self, secs=10):
		for motorname, motor in self.motors.items():
			self.run(motorname, 'F', 50,
				'testing hat %s motor %s at %s' % (self.name, motorname, 50))
		time.sleep(secs)
		self.shutdown()



if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	verbose = True

	hats = [Hat('0x67', [1,2,3,4], verbose=verbose),
			Hat('0x61', [1,2,3,4], verbose=verbose),
			Hat('0x60', [1,2,3,4], verbose=verbose),
			Hat('0x66', [1,2,3,4], verbose=verbose)]

	poll_interval = 1
	running = False
	sensed = False

	for i in [0,1,2,3]:
		for motorname, motor in hats[i].motors.items():
			hats[i].run(motorname, 'F', 75)
			time.sleep(10)
			hats[i].run(motorname, 'B', 75)
			time.sleep(10)
			hats[i].shutdown_one(motorname)
