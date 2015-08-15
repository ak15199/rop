#!/usr/bin/evn python

# PB, 22 Jul 2015
# from various bits of code

import time
import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

ARDUINO_PIN = 17
LAMP_PIN = 27
GPIO.setup(LAMP_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ARDUINO_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
	GPIO.output(ARDUINO_PIN, GPIO.HIGH)
except:
    pass

while 1:
    try:
    	time.sleep(1)

    except KeyboardInterrupt:
        GPIO.output(ARDUINO_PIN, GPIO.LOW)
        GPIO.output(LAMP_PIN, GPIO.LOW)
        GPIO.cleanup()

# end.