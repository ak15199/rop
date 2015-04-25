"""
Display Configuration
"""
# Display Geometry
WIDTH, HEIGHT = 32, 32

# Device type and address
ADDRESS='ansi-2'            # For display to the TTY
#ADDRESS='localhost:7890'   # OPC driver

# Device configuration
ZIGZAG=True                 # whether display reverses direction, line to line
#FLIPUD=True                # up-down display orientation
FLIPLR=True                 # left-right display orientation

"""
Art Configuration Settings
"""
config = {
    "GUARDIAN_APIKEY": "",  # See http://open-platform.theguardian.com/access/
    }
