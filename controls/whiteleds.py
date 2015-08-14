#!/usr/bin/evn python

# PB, 22 Jul 2015
# from various bits of code
# there's probably a way to do this without sitting in the loop.

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

LAMP_PIN = 13
GPIO.setup(LAMP_PIN, GPIO.OUT, initial=GPIO.LOW)
# pwm = GPIO.PWM(LAMP_PIN, 1000)
# pwm.start(95)
# start_time = time.time()

# def now():
# 	return time.time() - start_time

# class LED():
# 	def __init__(self, pwm):
# 		self.pwm = pwm
# 		self.endtime = None

# 	def setstate(self, dc, secs):
# 		# note: dc=50 is pretty bright. unlikely to need higher.
# 		self.endtime = now() + secs
# 		print("at %s, setting dc=%s for %s secs (endtime=%s)" % (now(), dc, secs, self.endtime))
# 		self.pwm.start(dc)

# 	def endstate(self):
# 		return self.endtime is None or now() > self.endtime


# led = LED(pwm)
# states = [(5,2), (0,1), (25, 2), (0, 1), (50,2)]
# state_pos = 0
# print("starting. CTRL+C to exit")

try:
	GPIO.output(LAMP_PIN, GPIO.HIGH)
	while 1:
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()

