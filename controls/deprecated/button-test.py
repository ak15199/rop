
import time
import os
import RPi.GPIO as GPIO

def shutdown(channel):
    print("%s: button! shutting down" % time.time())
    os.system("sudo shutdown -h now")

GPIO.setmode(GPIO.BCM)

BUTTON_PIN = 22

GPIO.setup(BUTTON_PIN, GPIO.IN, initial=GPIO.LOW)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
    callback=shutdown, bouncetime=500)

while 1:
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
