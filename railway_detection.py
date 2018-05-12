import RPi.GPIO as GPIO
import spidev
import time
import sys
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
LDAC = 35

spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setup(37, GPIO.IN)
GPIO.setup(LDAC,GPIO.OUT, initial=1)

#Interrupt routine
def my_callback(channel):
    print('GPS call')
    exec(open("gpsd.py").read())
   
#Add rising edge interrupt   
GPIO.add_event_detect(37, GPIO.RISING, callback=my_callback, bouncetime=300)

try:
    GPIO.output(LDAC, 1)             #LDAC on DAC goes HIGH
    spi.xfer([0x7F,0xFF],20000000)   #Transfer 7FFF at 20 MHz
    GPIO.output(LDAC, 0)             #LDAC on DAC goes LOW, input latches output at DAC
    GPIO.output(LDAC, 1)             #LDAC goes high again 
    while True:
            i = 1                    #Empty loop, do nothing
    GPIO.cleanup()
    sys.exit(0)
except:
    #spi.close()
    GPIO.cleanup()
    sys.exit(0)

