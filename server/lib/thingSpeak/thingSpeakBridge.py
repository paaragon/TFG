import httplib
import urllib
import time
import paho.mqtt.publish as publish

def sendToThingSpeak(data):

    headers = {"Content-typZZe": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    params = urllib.urlencode(data)
    conn = httplib.HTTPConnection("api.thingspeak.com:80")

    try:

        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()

        print 'Result of conection: ', response.status, response.reason

        data = response.read()

        print 'Records in thingSpeak: ', data

        conn.close()

    except:
        print "connection failed"

def sendToManuel(radiation):
    channelID = "281569"
    apiKey = "GSUF8ZCW1D0RO0MB"
    mqttHost = "mqtt.thingspeak.com" 
    tTransport = "tcp"
    tPort = 1883
    tTLS = None
    topic = "channels/" + channelID + "/publish/" + apiKey
    tPayload = "field7=" + str(radiation)
    try:
        publish.single(topic,payload=tPayload,hostname=mqttHost,port=tPort,tls=tTLS,transport=tTransport)
        print "Send to Manuel Broker"
    except:
        print "Error connecting to Manuel thingspeak"
    #headers = {"Content-typZZe": "application/x-www-form-urlencoded",
    #           "Accept": "text/plain"}

    #thingSpeakData = {
    #    'field7': radiation,
    #    'key': 'GSUF8ZCW1D0RO0MB'
    #}

    #params = urllib.urlencode(data)
    #conn = httplib.HTTPConnection("api.thingspeak.com:80")

    #try:

        #conn.request("POST", "/update", params, headers)
        #response = conn.getresponse()

        #print response.status, response.reason

        #data = response.read()

        #print data

        #conn.close()

    #except:
    #    print "connection failed"


if __name__ == "__main__":

    from random import randint
    for i in range(0, 30):
        data = {'field4': randint(0, 500), 'key': 'O2M7W8NYQL5X7XD3'}
        sendToThingSpeak(data)
        time.sleep(16)
