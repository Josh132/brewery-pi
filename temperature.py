import os
import glob
import time
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)#RED
GPIO.setup(22,GPIO.OUT)#GREEN
GPIO.setup(27,GPIO.OUT)#BLUE


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


# Read temperature from device

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines=read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.1)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c#, temp_f

# Open file to be logged

file = open("/home/pi/Desktop/Templog.csv", "a")

if os.stat("/home/pi/Desktop/Templog.csv").st_size == 0:
    file.write("Date, Time, TemperatureSensor1\n")

# Continuous loop
while True:
    print(read_temp())
    if(read_temp()<25):
       GPIO.output(17,GPIO.LOW)
       GPIO.output(22,GPIO.HIGH)

    else:
       GPIO.output(17,GPIO.HIGH)
       GPIO.output(22,GPIO.LOW)

    now = datetime.now()
    file.write(str(now.day)+"-"+str(now.month)+"-"+str(now.year)+","+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+","+str(read_temp())+"\n")
    file.flush()
    time.sleep(5)
