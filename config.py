"""
Display Configuration
"""
# Display Geometry
WIDTH, HEIGHT = 32, 32

# Device type and address, where 'address' is an optional colon-separated
# part of the value that is driver dependent
DRIVER='ansi'                # For display to the TTY
#DRIVER='opc:localhost:7890' # OPC driver

# Device configuration
#ZIGZAG=True                 # whether display reverses direction, line to line
#FLIPUD=True                 # up-down display orientation
#FLIPLR=True                 # left-right display orientation

"""
Art Configuration Settings
"""
config = {
    "GUARDIAN_APIKEY": "",   # See http://open-platform.theguardian.com/access/
    }
