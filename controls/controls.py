#!/usr/bin/python
#
# controls.py
#
# opens rotating file handler
# reads distance, voltage, current
##   maybe by 3 threads each taking 100 samples
##   take time-weighted average?
# checks voltage: off if <11.1, log, shutdown, set long sleep (120s), continue
# check distance: if presence, reset run_until +60s from now
# if time.time() < run_until: check motors,

import time, signal, sys
sys.path.append("/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_ADS1x15")
from Adafruit_ADS1x15 import ADS1x15

def signal_handler(signal, frame):
        #print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C to exit'

ADS1015 = 0x00  # 12-bit ADC
adc = ADS1x15(ic=ADS1015)

V_per_mV_read = 63.69
A_per_mV_read = 3.7

while True:
    # Read channels 2 and 3 in single-ended mode, at +/-4.096V and 250sps
    sensors = {'volts': adc.readADCSingleEnded(0, 4096, 250),
               'amps':  adc.readADCSingleEnded(1, 4096, 250),
               'dist':  adc.readADCSingleEnded(2, 4096, 250),
               'gnd':   adc.readADCSingleEnded(3, 4096, 250),
               'amps2': adc.readADCDifferential(chP=1, chN=3)
              }

    print(sensors)

    # print "v0=%s, v1=%s, v2=%s" % tuple(volts_single)
    meas_V = round(sensors['volts']/V_per_mV_read, 2)
    meas_A = round(sensors['amps']/A_per_mV_read, 2)
    meas_D = round(sensors['dist']/(5.3/512.0) , 0)
    #print "time: %s. measured A=%s, measured V=%s, measured D=%s" % (
    #    int(time.time()), meas_A, meas_V, meas_D)

    time.sleep(1)