'''
RASPBERRY PI TEMPERATURE CONTROLL FOR BEER FRIDGE
'''

import os
import glob
import time
import RPi.GPIO as GPIO
from datetime import datetime
from tkinter import *


#Set gpio's
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)#RED
GPIO.setup(22,GPIO.OUT)#GREEN
GPIO.setup(27,GPIO.OUT)#BLUE
GPIO.setup(5,GPIO.OUT)#RELAY
GPIO.output(5,GPIO.HIGH)
GPIO.output(17,GPIO.LOW)
GPIO.output(22,GPIO.LOW)
GPIO.output(27,GPIO.LOW)


#grab temp probe information
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


temp = read_temp()
desiredtemp = 17
deg = u'\xb0'#utf code for degree
relay = "N/A"


#increase button press
def increase():
    global desiredtemp
    desiredtemp += 0.5
    tmpstr.set("%s" % desiredtemp)
   

#Decrease button press
def decrease():
    global desiredtemp
    desiredtemp -= 0.5
    tmpstr.set("%s" % desiredtemp)


   
#Tkinter start
root = Tk()
root.wm_title("Beer Temp") #Name the title bar

#code to add widgets will go here....

#make 3 frames for text and buttons
topFrame = Frame(root)
topFrame.pack(side=TOP)

middleFrame = Frame(root)
middleFrame.pack()

midlowFrame = Frame(root)
midlowFrame.pack()
   
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

#Variables for tkinter
tmpstr = StringVar(value="%s" % desiredtemp)
crtmpstr = StringVar(value="%s" % temp)
relaystatus = StringVar(value="%s" % relay)

#Set labels
label1 = Label(topFrame, text="Desired Temp = ", fg="black")
label2 = Label(middleFrame, text="Actual Temp = ", fg="black")
label3 = Label(topFrame, textvariable=tmpstr, fg="black")
label4 = Label(midlowFrame, text="Relay = ", fg="purple")
label5 = Label(midlowFrame, textvariable=relaystatus, fg="purple")
label6 = Label(middleFrame, textvariable=crtmpstr, fg="black")


#use to put labels on screen
label1.pack(side=LEFT)
label2.pack(side=LEFT)
label3.pack(side=LEFT)
label4.pack(side=LEFT)
label5.pack(side=LEFT)
label6.pack(side=LEFT)

#Set buttons
button1 = Button(bottomFrame, text="Increase (0.5"+ deg +"C)", fg="darkgreen", command=increase)
button2 = Button(bottomFrame, text="Decrease (0.5"+ deg +"C)", fg="red", command=decrease)

#use to put buttons on screen
button1.pack(side=LEFT)
button2.pack(side=LEFT)


# Open file to be logged
'''
file = open("/home/pi/Desktop/Templog.csv", "a")

if os.stat("/home/pi/Desktop/Templog.csv").st_size == 0:
    file.write("Date, Time, TemperatureSensor1\n")

'''

# Continuous print loop
while True:
    #print(read_temp())
    if(read_temp()>=desiredtemp):
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(5,GPIO.HIGH)
        GPIO.output(22,GPIO.LOW)
        crtmpstr.set("%s" % read_temp())
        relay="ON"
        relaystatus.set("%s" % relay)
    else:
        GPIO.output(17,GPIO.LOW)
        GPIO.output(5,GPIO.LOW)
        GPIO.output(22,GPIO.HIGH)
        crtmpstr.set("%s" % read_temp())
        relay="OFF"
        relaystatus.set("%s" % relay)

    '''now = datetime.now()
    file.write(str(now.day)+"-"+str(now.month)+"-"+str(now.year)+","+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+","+str(read_temp())+"\n")
    file.flush()'''
    time.sleep(0.5)
    root.update()
   
   
root.mainloop()


