"""
Display Configuration
"""

import serial
import traceback
import json

PORT = '/dev/ttyAMA0'

def event_generator():
    ser = None
    buffer = []

    while True:
        if not ser:
            try:
                ser = serial.Serial(baudrate=9600, port=PORT)
            except OSError:
                ser = None
            else:
                ser.timeout = 1
                print 'serial connected'
        if not ser:
            yield None
            continue
        try:
            while ser.inWaiting():
                try:
                    c = ser.read()
                    if c == '\r': continue
                    elif c == '\n':
                        text = ''.join(buffer)
                        yield json.loads(text)
                        buffer[:] = []
                    else:
                        buffer.append(c)
                except:
                    print text
                    traceback.print_exc()
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
    'BRIGHTNESS_THRESHOLD': 100,        # Between and 255, pixels must be so bright to be "seen"
    'FADE': (0.90, 0.99),               # Fadeout speed per iteration (low, high)
    'MOVEMENT_TIMEOUT': 5,              # In seconds
    'CONTROL_TIMEOUT': 2,               # How long controls linger
    'COLOR_ROTATION': (0.005, 0.1),     # Color rotation speed per iteration (low, high)
    'MIN_MOVE_COUNT': 10,               # Minimum number of pixels to trigger movement sense
    'MIN_SLEEP_TIME': 5,                # Minimum number of seconds to enter dream state
    'MIN_WAKE_MOVE': 10,                # Minimum number of frames must see movement to awake
    'ARTS': {
        'TIMEOUT': 5,
        'COMPOUND': [
            ('drops', {
               'DROP_CHANCE': 0.3,       # Chance each frame of new drop - hight == more drops
               'DROP_SPEED': (0.2, 0.4), # Drop speed (min, max) value between 0.0 and 1.0
               'DROP_FADE': 0.95,        # Number between 0.0 and 1.1 - higher means longer trails
            }),
            ('persistent', {
                'COMPOUND': [
                    ('psyblobs', {}),
                ],
            }),
            ('life', {'HSCALE': 0.025, 'ITERATIONS': 10000}),
            #('spill', {}),
            #('rotor', {}),
            ('race', {}),
            ('pops', {}),
        ],
    },
}
