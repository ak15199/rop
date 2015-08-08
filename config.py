"""
Display Configuration
"""

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
    "COMPOUND": [
        ('persistent', {
            "COMPOUND": [
                ('shift', {'dv': 0.97}),
                ('mirror', {
                    'BRIGHTNESS_THRESHOLD': 50,
                    'FADE': 0.92
                }),
            ]
        })
    ]
}
