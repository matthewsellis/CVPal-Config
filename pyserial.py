import time
import serial
"""
Working Command/response sets

INP>> *IDN?
OUT>>OWON,XDM1041,2153543,V3.1.0,3

INP>> MEAS?
OUT>>-8.975894E-05

INP>> MEAS1?
OUT>>-7.065640E-05

INP>> MEAS2?
OUT>>NONe

INP>> RANGe?
OUT>>50 V

INP>> SYSTem:REMote
INP>> SYSTem:LOCal
INP>> CONFigure:VOLTage:AC
INP>> CONFigure:VOLTage:DC 50
INP>> SYSTem:REMote
INP>> MEAS1?
OUT>>3.215547E-05

INP>> MEAS?
OUT>>9.655420E+00

"""
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/tty.usbserial-110',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

inp=''
while 1 :
    # get keyboard input
    inp = input("INP>> ")

    if inp == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        inp += '\n'
        ser.write(inp.encode())

        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1).decode()
            
        if out != '':
            print( "OUT>>" + out )
