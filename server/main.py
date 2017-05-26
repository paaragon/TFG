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
    #try:
    data = json.loads(msg.payload)

    # make prediction and add it to data dictionary
    data['prediction'] = predict.getPrediction(data['date'],
                                                data['ubication'],
                                                data['temperature'],
                                                data['humidity'],
                                                data['radiation'])

    print data['date']
    print data['ubication']
    print data['temperature']
    print data['humidity']
    print data['radiation']
    print data['prediction']

    # create dictionary to send to thingSpeak
    thingSpeakData = {
        'field1': data['date'],
        'field2': data['ubication'],
        'field3': data['temperature'],
        'field4': data['humidity'],
        'field5': data['radiation'],
        'field6': data['prediction'],
        'key': thingspeakKey
    }

    thingSpeakBridge.sendToThingSpeak(thingSpeakData)

    #except ValueError as e:
    #    print('%s' % e)


if __name__ == "__main__":

    mqttClient.set_on_message(mqtt_listen_function)
    mqttClient.listenToBroker(brokerIp, brokerPort, topic)
