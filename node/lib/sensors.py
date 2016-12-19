#!/usr/bin/env python

import wiringpi as wiringpi
import Adafruit_DHT
import time

wLedPin = 2 # Wirin pin mode
wDHTPin = 4 # GPIO pin mode

wiringpi.wiringPiSetup()
wiringpi.pinMode(wLedPin, 1)
wiringpi.pinMode(wDHTPin, 0)

def led(state):

    if state == "off":
        wiringpi.digitalWrite(wLedPin, 1)

    elif state == "on":
        wiringpi.digitalWrite(wLedPin, 0)

def dht():

    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, wDHTPin)


#
# return - JSOn with humidity and temperature keys
#
def readDHT(ledOn=True):

    if ledOn:
        led("on")
    
    humidity, temperature = dht()

    led("off")

    if humidity is not None and temperature is not None:
	return '{"temperature": '+str(format(temperature, '.2f'))+', "humidity": '+str(format(humidity, '.2f'))+'}'

    else:
        return '{"temperature": null, "humidity": null}'

if __name__ == "__main__":

    led("on")

    humidity, temperature = dht()
    if humidity is not None and temperature is not None:
        print '{"temperature": '+str(format(temperature, '.2f'))+', "humidity": '+str(format(humidity, '.2f'))+'}'
    else:
        print "Fail reading"
    time.sleep(0.5)

    led("off")
