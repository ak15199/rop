#!/usr/bin/python
#
# :Author: PB
# :Date: 4 Aug 2015
# :License: GPL v2
#
# motor controller for k Hats with a list of motors on each Hat
#
# Todo:
#  -- add polling for sensors on ADC (see cmtd code)
#  -- what process for determining presence? average last second?
#  -- write poll result to sensor file
#  -- switch motor action from file polling to presence calc.
#  -- control illumination lights? slow up, slow down. (whiteleds.py)
#


import time
import json
import collections
import os
import atexit
import os
import random
import signal
import sys

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
sys.path.append("/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_ADS1x15")
from Adafruit_ADS1x15 import ADS1x15
ADS1015 = 0x00  # 12-bit ADC


def handle_INT(signal, frame):
    print("SIGINT caught, exiting gracefully.")
    shutdown(quit=True)

def handle_TERM(signal, frame):
    print("SIGTERM caught, exiting gracefully.")
    halt()

def halt(ignore=None):
    shutdown(quit=True, halt=True)

<<<<<<< HEAD
def turnon_arduino():
    GPIO.output(ARDUINO_PIN, GPIO.HIGH)

def shutdown_arduino():
    GPIO.output(ARDUINO_PIN, GPIO.LOW)

def turnon_lamp():
    GPIO.output(LAMP_PIN, GPIO.HIGH)

def shutdown_lamp():
    GPIO.output(LAMP_PIN, GPIO.LOW)

def shutdown_motors():
    for hat in hats:
        hat.shutdown()


def shutdown(quit=False, halt=False):
    shutdown_motors()
    shutdown_arduino()
    shutdown_lamp()
    GPIO.cleanup()
    if halt:
        os.system("sudo shutdown -h now")
    if quit or halt:
        sys.exit(0)
=======
def shutdown(quit=False, halt=False):
	log_rec = {'timestamp': int(time.time()),
				'message': "shutting down IR lamp and motors."}
	with open(logfile, 'a') as logFH:
		logFH.write("%s\n" % json.dumps(log_rec))
	with open('/home/pi/var/spool/ir-dutycycle', 'r') as dcFH:
		dcFH.write("0\n")
	for hat in hats:
		hat.shutdown()
	if halt:
	    os.system("sudo shutdown -h now")
	if quit or halt:
		sys.exit(0)
>>>>>>> b658a44da7d0f428a9677a9b578b1d631cbbc5e9


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
<<<<<<< HEAD
    signal.signal(signal.SIGINT, handle_INT)
    signal.signal(signal.SIGTERM, handle_TERM)

    GPIO.setup(LAMP_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ARDUINO_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(BUTTON_PIN, GPIO.IN, initial=GPIO.LOW)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
        callback=halt, bouncetime=500)

    verbose = True

    ADS1015 = 0x00  # 12-bit ADC
    adc = ADS1x15(ic=ADS1015)
    V_per_mV_read = 200.8

    hats = [Hat('0x67', [1,2,3,4], verbose=verbose),
            Hat('0x61', [1,2,3,4], verbose=verbose),
            Hat('0x60', [1,2,3,4], verbose=verbose),
            Hat('0x66', [1,2,3,4], verbose=verbose)]

    poll_interval = 1
    running = False
    sensed = False
    log_rec = dict()
    voltages = collections.deque(maxlen=100)
    logfile = "/home/pi/var/log/%s.log" % datetime.datetime.now().isoformat().replace(':', '-').split('.')[0]
    with open(logfile, 'w') as logFH:
        logFH.write('# beginning log')

    while True:
        volts = adc.readADCSingleEnded(0, 4096, 250)
        measured_V = round(volts/V_per_mV_read, 2)
        # sensors = {'volts': adc.readADCSingleEnded(0, 4096, 250),
        #            'dist':  adc.readADCSingleEnded(3, 4096, 250)
        #           }
        # print "v0=%s, v1=%s, v2=%s" % tuple(volts_single)
        # measured_V = round(sensors['volts']/V_per_mV_read, 2)
        # measured_D = round(sensors['dist']/(5.3/512.0) , 0)
        voltages.append(measured_V)
        mean_V = sum(voltages)/len(voltages)
        # print "time: %s. measured V=%s, measured D=%s" % (
        #    int(time.time()), measured_V, measured_D)

        log_rec = {'timestamp': int(time.time()),
                    'running': running, sensed: sensed,
                    'last_volts': volts, 'mean_volts': mean_V}
        with open(logfile, 'a') as logFH:
            logFH.write(json.dumps(log_rec))

        # now take action.
        if mean_V < 11.1:
            halt()

        # change this to poll sensor then write to sensed.
        with open("/home/pi/sensed", 'r') as presence:
            sensed = presence.read().strip()[-1]

        if sensed not in ["0", "1"] or sensed == "0":
            if running:
                shutdown(quit=False)
            running = False
            time.sleep(poll_interval/2.0)
            continue

        if not running:
            # startup code: bring up IR light, then start motors
            running = True
            turnon_lamp()

        for hat in hats:
            hat.check_all_and_restart()

        # here log what's going on: lamp, sensed, voltage, motor status
        time.sleep(poll_interval) # possible to go slower?

    shutdown(quit=True)
=======
	signal.signal(signal.SIGINT, handle_INT)
	signal.signal(signal.SIGTERM, handle_TERM)

	verbose = True

	ADS1015 = 0x00  # 12-bit ADC
	adc = ADS1x15(ic=ADS1015)
	V_per_mV_read = 200.8

	IR_VALUE = 100  # tune this

	hats = [Hat('0x67', [1,2,3,4], verbose=verbose),
			Hat('0x61', [1,2,3,4], verbose=verbose),
			Hat('0x60', [1,2,3,4], verbose=verbose),
			Hat('0x66', [1,2,3,4], verbose=verbose)]

	poll_interval = 1
	running = False
	sensed = False
	log_rec = dict()
	voltages = collections.deque(maxlen=100)

	# needs to rotate the status.log to its timestamp
	logpath = "/home/pi/var/log/status.log"
	logstat = os.stat(logpath)
 	newpath = "/home/pi/var/log/%s.log" % time.strftime("%Y-%m-%d-%H.%M.%SZ", time.gmtime(logstat))
 	os.rename(logpath, newpath)
	with open(logpath, 'w') as logFH:
		logFH.write('# beginning log')

	while True:
	    sensors = {'volts': adc.readADCSingleEnded(0, 4096, 250),
	               'dist':  adc.readADCSingleEnded(3, 4096, 250)
	              }
	    # print "v0=%s, v1=%s, v2=%s" % tuple(volts_single)
	    measured_V = round(sensors['volts']/V_per_mV_read, 2)
	    measured_D = round(sensors['dist']/(5.3/512.0) , 0)
	    voltages.append(measured_V)
	    mean_V = sum(voltages)/len(voltages)
	    # print "time: %s. measured V=%s, measured D=%s" % (
	    #    int(time.time()), measured_V, measured_D)

		log_rec = {'timestamp': int(time.time()),
					'running': running, 'sensed': sensed,
					'volts': mean_V, 'distance': meas_D}
		with open(logpath, 'a') as logFH:
			logFH.write("%s\n" % json.dumps(log_rec))

		# now take action.
		if mean_V < 11.1:
			log_rec = {'timestamp': int(time.time()),
						'message': "mean volts too low, shutting down."}
		with open(logpath, 'a') as logFH:
			logFH.write("%s\n" % json.dumps(log_rec))
			shutdown(quit=True, halt=True)
			# shut it down!
			time.sleep(poll_interval * 10)
			continue

		# todo:
	 	# might want to leave motors running all the time.
	 	# would require rethinking shutdown()
		with open("/home/pi/var/spool/sensed", 'r') as presence:
			sensed = presence.read().strip()[-1]

	 	if sensed not in ["0", "1"] or sensed == "0":
			if running:
				shutdown(quit=False)
				running = False
			time.sleep(poll_interval/2.0)
			continue

		if not running:
	 		# startup code: bring up IR light, then start motors
			running = True
			with open('/home/pi/var/spool/ir-dutycycle', 'r') as dcFH:
				dcFH.write("%s\n" % IR_VALUE)

		for hat in hats:
			hat.check_all_and_restart()

		# here log what's going on: lamp, sensed, voltage, motor status
		time.sleep(poll_interval) # possible to go slower?

	shutdown(quit=True)
>>>>>>> b658a44da7d0f428a9677a9b578b1d631cbbc5e9
