# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:25:16 2016

@author: slide22
"""

import paho.mqtt.client as mqtt
import json

def sendToBroker(brokerIp, brokerPort, payload, topic):
    
    client = mqtt.Client()
    client.connect(brokerIp, brokerPort, 60)
    
    client.publish(topic, payload=payload)
    
    client.disconnect()
    print "Succesfully published"

def listenToBroker(brokerIp, brokerPort, topic):
    

if __name__ == "__main__":
    data = {"codigo": 1,\
            "ubicación": "Navas de Arévalo"}
    sendToBroker("127.0.0.1", 1883, json.dumps(data), "solar")
