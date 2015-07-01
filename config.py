"""
Display Configuration
"""
# Display Geometry
WIDTH, HEIGHT = 40, 50

# Device type and address, where 'address' is an optional colon-separated
# part of the value that is driver dependent
DRIVER = 'sdl2window'                # For display to the TTY
# DRIVER = 'opc:localhost:7890' # OPC driver

# Device configuration
# ZIGZAG = True                 # whether display reverses direction, line to line
# FLIPUD = True                 # up-down display orientation
# FLIPLR = True                 # left-right display orientation

selection = 0
def selector(new=None):
    global selection
    if new != None:
        selection = new
    return selection


"""
Art Configuration Settings
"""
config = {
    "COMPOUND": [
        ('persistent', {
            "COMPOUND": [
                ('fade', {}),
                ('selector', {
                    "COMPOUND": [
                        ('life', {}),
                        ('mirror', {}),
                    ],
                    "SELECTOR": selector,
                }),
            ]
        }),
        ('rotator', {
            "SELECTOR": selector,
            "TIMEOUT": 5,
        })
    ]
}
