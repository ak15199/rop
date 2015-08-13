import serial
ser = serial.Serial('/dev/ttyAMA0', 9600)

while 1 :
    line = ser.read(1024*1024)
    print(line)
