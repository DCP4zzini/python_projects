from datetime import datetime
import serial
import csv
import time

# Serial instance
ser = serial.Serial('COM3', 38400, timeout=0.1)
MAX_NUMBER_OF_MEASURES = 100
MAX_TIME_INTERVAL = 10
number_of_measures = 0

print("Device connected:", ser.name, "port")
time.sleep(1)

user_number_of_measurements = int(input("Insert the number of measurements you want to collect --> MAX 100 samples: \n\r"))
# Check the user input
user_number_of_measurements = user_number_of_measurements if ( user_number_of_measurements < MAX_NUMBER_OF_MEASURES and user_number_of_measurements > 0) else MAX_NUMBER_OF_MEASURES
user_time_interval = int(input("Insert the time interval from each measurement (in seconds) -- Min = 0 | Max = 10 -- : \n\r"))
# Check the user input
user_time_interval = user_time_interval if ( user_time_interval < MAX_TIME_INTERVAL) else MAX_TIME_INTERVAL

with open('data_exportation.csv', 'w', newline='') as csv_file:
    csvwriter = csv.writer(csv_file)

    while user_number_of_measurements > 0 :

        #wake up command sent to mcu
        ser.write(b'wake up')
        time.sleep(0.001)
        data_buffer = ser.readline()

        #Check. If there is an error, ignore the colected value
        if(data_buffer.decode('utf-8') != ''):
            print(data_buffer.decode('utf-8'))
            time_stamp = datetime.now()
            data_buffer = "ADC Value: " + str(data_buffer.decode('utf-8')) + " | Time: " + time_stamp.strftime('%H:%M:%S')
            csvwriter.writerow([data_buffer])
            user_number_of_measurements -= 1

        #interval time according to user input
        time.sleep(user_time_interval)

ser.close()
print("Data exported to .csv format, finishing app...")

