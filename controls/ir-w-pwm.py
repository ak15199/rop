#!/usr/bin/evn python

# PB, 22 Jul 2015
# from various bits of code
# 17 Aug 2015 rewritten for the IR lamp using hardware PWM

import time
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


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_INT)
    signal.signal(signal.SIGTERM, handle_TERM)

    GPIO.setmode(GPIO.BCM)
    # Pin setup
    LAMP_PIN = 18   # Broadcom pin 18 (P1 pin 12)
    GPIO.setup(LAMP_PIN, GPIO.OUT) # PWM pin set as output
    pwm = GPIO.PWM(LAMP_PIN, 50)  # Initialize PWM on pwmPin 100Hz frequency

    poll_interval = 0.5
    val = 0

    while True:
        with open('/home/pi/var/spool/ir-dutycycle', 'r') as dcFH:
            data = dcFH.read().strip()
        try:
            new_val = int(data)
        except ValueError:
            pass # val stays the same
        if 0 <= val and val <= 100 and val != new_val:
            val = new_val
            pwm.ChangeDutyCycle(val)
        time.sleep(poll_interval)


    # end.