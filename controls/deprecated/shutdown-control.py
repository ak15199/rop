
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 22

GPIO.setup(BUTTON_PIN, GPIO.IN, initial=GPIO.LOW)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
    callback=halt, bouncetime=500)

while True:
    sleep(1)
