#-*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:25:16 2016

@author: slide22
"""

import paho.mqtt.client as mqtt


def listen_on_connect(client, userdata, rc):
    print "Connected with result code " + str(rc)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("solar")


def listen_on_message(client, userdata, msg):
    print msg.topic + " " + str(msg.payload)


def sendToBroker(brokerIp, brokerPort, payload, topic):

    client = mqtt.Client()
    client.connect(brokerIp, brokerPort, 60)

    result = client.publish(topic, payload=payload)
    if result[0] == mqtt.MQTT_ERR_NO_CONN:
        return False

    client.disconnect()
    return True


def listenToBroker(brokerIp, brokerPort, topic):

    client = mqtt.Client()
    client.on_connect = listen_on_connect
    client.on_message = listen_on_message

    client.connect(brokerIp, brokerPort, 60)

    client.loop_forever()


if __name__ == "__main__":

    listenToBroker("127.0.0.1", 1883, "solar")
