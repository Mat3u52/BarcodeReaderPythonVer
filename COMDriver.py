# import serial
#
# class COMDriver:
#
#     def __init__(self):



# ser = serial.Serial()
# #ser.port = "/dev/ttyUSB0"
# ser.port = "/dev/ttyUSB7"
# #ser.port = "/dev/ttyS2"
# ser.baudrate = 9600
# ser.bytesize = serial.EIGHTBITS #number of bits per bytes
# ser.parity = serial.PARITY_NONE #set parity check: no parity
# ser.stopbits = serial.STOPBITS_ONE #number of stop bits
# #ser.timeout = None          #block read
# ser.timeout = 1            #non-block read
# #ser.timeout = 2              #timeout block read
# ser.xonxoff = False     #disable software flow control
# ser.rtscts = False     #disable hardware (RTS/CTS) flow control
# ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
# ser.writeTimeout = 2     #timeout for write
