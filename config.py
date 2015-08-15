"""
Display Configuration
"""

import serial
import traceback
import json

def event_generator():
    ser = None
    buffer = []

    while True:
        if not ser:
            try:
                ser = serial.Serial(baudrate=9600, port='/dev/cu.usbserial-A101KWG0')
            except OSError:
                ser = None
        if not ser:
            yield None
            continue
        try:
            while ser.inWaiting():
                c = ser.read()
                if c == '\r': continue
                elif c == '\n':
                    text = ''.join(buffer)
                    try:
                        yield json.loads(text)
                    except:
                        print text
                        traceback.print_exc()
                    buffer[:] = []
                else:
                    buffer.append(c)
        except IOError:
            ser = None
        yield None

ENV = 'dev'  # 'dev' == development environment,  'prod' == production environment

# Display Geometry
# Dimensions of mirror is 4x6
WIDTH, HEIGHT = 32, 50

# Device type and address, where 'address' is an optional colon-separated
# part of the value that is driver dependent
DRIVER = 'opc:localhost:7890'

# Device configuration
# ZIGZAG = True                 # whether display reverses direction, line to line
# FLIPUD = True                 # up-down display orientation
# FLIPLR = True                 # left-right display orientation


"""
Art Configuration Settings
"""
config = {
    "EVENTS": event_generator(),
    "COMPOUND": [
        ('persistent', {
            "COMPOUND": [
                ('shift', {'dv': 0.97}),
                ('mirror', {
                    'BRIGHTNESS_THRESHOLD': 100,
                    'FADE': 0.92,
                    'COLOR_ROTATION': 0.05,
                    "EVENTS": event_generator(),
                }),
            ]
        })
    ],
    'BRIGHTNESS_THRESHOLD': 100,
    'FADE': 0.92,
    'COLOR_ROTATION': 0.05,
}
