# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:25:16 2016

@author: slide22
"""

import paho.mqtt.client as mqtt

client = mqtt.Client()


def listen_on_connect(client, userdata, rc):
    print "Connected with result code " + str(rc)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("solar")


def sendToBroker(brokerIp, brokerPort, payload, topic):

    client.connect(brokerIp, brokerPort, 60)

    client.publish(topic, payload=payload)

    client.disconnect()
    print "Succesfully published"


def listenToBroker(brokerIp, brokerPort, topic):

    client.on_connect = listen_on_connect

    client.connect(brokerIp, brokerPort, 60)

    client.loop_forever()


def set_on_message(function):
    client.on_message = function


if __name__ == "__main__":

    listenToBroker("127.0.0.1", 1883, "solar")
