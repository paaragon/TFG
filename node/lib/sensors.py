#!/usr/bin/env python

import wiringpi as wiringpi
import Adafruit_DHT
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

wLedPin = 2 # Wirin pin mode
wDHTPin = 4 # GPIO pin mode

wiringpi.wiringPiSetup()
wiringpi.pinMode(wLedPin, 1)
wiringpi.pinMode(wDHTPin, 0)
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



def led(state):

    if state == "off":
        wiringpi.digitalWrite(wLedPin, 1)

    elif state == "on":
        wiringpi.digitalWrite(wLedPin, 0)

def dht():

    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, wDHTPin)

def readDyn():
    mv = mcp.read_adc(0) * 3300.0 / 1024.0
    return mv * 0.5 #W*m^-2

#
# return - temperature and humidity
#
def readDHT(ledOn=True):

    if ledOn:
        led("on")
    
    humidity, temperature = dht()

    led("off")

    return temperature, humidity

if __name__ == "__main__":

    #led("on")

    humidity, temperature = dht()
    if humidity is not None and temperature is not None:
        print '{"temperature": '+str(format(temperature, '.2f'))+', "humidity": '+str(format(humidity, '.2f'))+'}'
    else:
        print "Fail reading"

    time.sleep(0.5)

    #led("off")

    while True:
        print readDyn()
        time.sleep(1)
