import json
import time
import pandas as pd
import os
from random import randint
from lib.mqtt import mqttClient
from lib.prediction import predict
from lib.thingSpeak import thingSpeakBridge

brokerIp = "solarcasting.dacya.ucm.es"
brokerPort = 1883
topic = "solar"
thingspeakKey = "O2M7W8NYQL5X7XD3"


def mqtt_listen_function(client, userdata, msg):

    # retriev data from MQTT server
    data = json.loads(msg.payload)

    datet = datetime.strptime(data['time'], '%d-%m-%Y %H:%M:%S')

    date = int(str(datet.year) + str(datet.month).zfill(2) + str(datet.day).zfill(2))
    hour = int(str(datet.hour).zfill(2) + str(datet.minute).zfill(2))
    recordsPath = 'data/records'+ str(date) +'.csv'

    # make prediction and add it to data dictionary
    data['prediction'] = predict.getPrediction(
                                recordsPath,
                                data['ubication'],
                                date,
                                hour,
                                data['temperature'],
                                data['humidity'],
                                data['radiation']
                            )[0]

    print data['time']
    print data['ubication']
    print data['temperature']
    print data['humidity']
    print data['radiation']
    print data['prediction']

    with open('data/records'+ str(date) +'.csv', 'a') as outfile:
        outfile.write("%s,%s,%i,%i,%i,%i\n" % (
            data['time'],
            data['ubication'],
            data['temperature'],
            data['humidity'],
            data['radiation'],
            data['prediction']
        ))

    # create dictionary to send to thingSpeak
    thingSpeakData = {
        'field1': data['time'],
        'field2': data['ubication'],
        'field3': data['temperature'],
        'field4': data['humidity'],
        'field5': data['radiation'],
        'field6': data['prediction'],
        'key': thingspeakKey
    }

    thingSpeakBridge.sendToThingSpeak(thingSpeakData)

# test for the day 20150101 recorded at 15:30
def test():
    from datetime import datetime
    # retriev data from MQTT server

    data = dict()
    data['ubication'] = 1
    data['temperature'] = 8.84
    data['humidity'] = 47.1
    data['radiation'] = 227.9
    data['time'] = "01-01-2015 15:30:00"

    # make prediction and add it to data dictionary
    datet = datetime.strptime(data['time'], '%d-%m-%Y %H:%M:%S')

    date = int(str(datet.year) + str(datet.month).zfill(2) + str(datet.day).zfill(2))
    hour = int(str(datet.hour).zfill(2) + str(datet.minute).zfill(2))
    recordsPath = 'data/records'+ str(date) +'.csv'

    data['prediction'] = predict.getPrediction(
                                recordsPath,
                                data['ubication'],
                                date,
                                hour,
                                data['temperature'],
                                data['humidity'],
                                data['radiation']
                            )[0]

    print data['prediction']

if __name__ == "__main__":

    #test()

    mqttClient.set_on_message(mqtt_listen_function)
    mqttClient.listenToBroker(brokerIp, brokerPort, topic)
