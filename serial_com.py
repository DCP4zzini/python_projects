import serial
import time

# Serial instance
ser = serial.Serial('COM3',\
                    38400, \
                    timeout=1 , #Important to keep different of zero, otherwise ser.read will not work as expected
                    )
data_buffer = " "

print("Device connected:", ser.name, "port")
time.sleep(1)

while True:
    #wake up comnand sent to mcu, waiting for the correct response
    ser.write(b'wake up')
    data_buffer = ser.read_until(b'\n')
    print("Stored data: ", data_buffer)
    #if data frame is the expected value
    if data_buffer == b'yes\n':
        print ("Packet Received")
        break

print("finishing app...")



