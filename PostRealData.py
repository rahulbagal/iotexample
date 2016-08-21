# Script will be used to read sensor data and then post the IoT Thinkspeak
# Read Temprature & Humidity using DHT11 sensor attached to raspberry PI
# Program posts these values to a thingspeak channel
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2
DEBUG = 1
# Define GPIO pin to which DHT11 is connected
DHTpin = 2
#Setup our API and delay
myAPI = "GET_YOUR_KEY"  # API Key from thingSpeak.com channel
myDelay = 15 #how many seconds between posting data
GPIO.setmode(GPIO.BCM)  

def getSensorData():
    print "In getSensorData";
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        TWF=((9.0/5*temperature)+32)
        print('TempF={0:0.1f}*F'.format(TWF))
    else:
        print('Failed to get reading. Try again!')
    return (str(humidity), str(temperature),str(TWF))


def main():
    print 'starting...'
    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    while True:
        try:
            print "Reading Sensor Data now"
            RHW, TW, TWF = getSensorData()
            print TW + " " + TWF+ " " + RHW + " "
            f = urllib2.urlopen(baseURL + "&field1=%s&field2=%s&field3=%s" % (TW, TWF, RHW))
            print f.read()
            f.close()
            sleep(int(myDelay))
        except Exception as e:
            print e
            print 'exiting.'
            break

# call main

if __name__ == '__main__':
    main()
