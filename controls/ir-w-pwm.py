#!/usr/bin/evn python

# PB, 22 Jul 2015
# from various bits of code
# 17 Aug 2015 rewritten for the IR lamp using hardware PWM

import time
import json
import sys
import signal
import RPi.GPIO as GPIO


def handle_INT(signal, frame):
    print("SIGINT caught, exiting gracefully.")
    shutdown()

def handle_TERM(signal, frame):
    print("SIGTERM caught, exiting gracefully.")
    shutdown()

def shutdown():
    pwm.stop() # stop PWM
    GPIO.cleanup() # cleanup all GPIO
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_INT)
    signal.signal(signal.SIGTERM, handle_TERM)

    GPIO.setmode(GPIO.BCM)
    # Pin setup
    # LAMP_PIN = 18   # Broadcom pin 18 (P1 pin 12)
    LAMP_PIN = 23
    GPIO.setup(LAMP_PIN, GPIO.OUT) # PWM pin set as output
    pwm = GPIO.PWM(LAMP_PIN, 50)  # Initialize PWM on pwmPin 100Hz frequency
    pwm.start(0)

    poll_interval = 0.5
    val = 0

    while True:
        with open('/home/pi/var/spool/ir-dutycycle', 'r') as dcFH:
            data = dcFH.read().strip()
	    # print("found %s in ir-dutycycle" % data)
        try:
            new_val = int(data)
        except ValueError:
            pass # val stays the same

        if 0 <= val and val <= 100 and val != new_val:
	    print("found new dutycycle value = %s" % new_val)
            log_rec = {'timestamp': int(time.time()),
                   'old_lamp_DC': val, 'new_lamp_DC': new_val}
            with open("/home/pi/var/log/status.log", 'a') as logFH:
                logFH.write("%s\n" % json.dumps(log_rec))
            val = new_val
            pwm.ChangeDutyCycle(val)
        time.sleep(poll_interval)

    # end.
