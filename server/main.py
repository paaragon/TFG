import json
import time
from random import randint
from lib.mqtt import mqttClient
from lib.thingSpeak import thingSpeakBridge

brokerIp = "192.168.1.135"
brokerPort = 1883
topic = "solar"

def mqtt_listen_function(client, userdata, msg):

    data = json.loads(msg.payload)
    print data['temperature']
    print data['humidity']

    #
    # Obtener la temperatura, humedad y radiacion actuales
    # Obtener una prediccion en base a los datos actuales
    #
    # Obtener la hora de la prediccion anterior
    # enviar los datos actuales con la prediccion que se hizo
    #

    data['created_at'] = time.time()
    data['radiation'] = randint(100, 200)
    data['prediction'] = randint(100, 200)

    thingSpeakData = {
        'field1': data['created_at'],
        'field2': data['ubication'],
        'field3': data['temperature'],
        'field4': data['humidity'],
        'field5': data['radiation'],
        'field6': data['prediction'],
        'key': 'O2M7W8NYQL5X7XD3'
        }

    thingSpeakBridge.sendToThingSpeak(thingSpeakData)

    
if __name__ == "__main__":

    mqttClient.set_on_message(mqtt_listen_function)
    mqttClient.listenToBroker(brokerIp, brokerPort, topic)
    
