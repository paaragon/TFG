import json
import time
import pandas as pd
from random import randint
from pathlib import Path
from lib.mqtt import mqttClient
from lib.prediction import predict
from lib.thingSpeak import thingSpeakBridge

brokerIp = "192.168.1.135"
brokerPort = 1883
topic = "solar"
thingspeakKey = "O2M7W8NYQL5X7XD3"

def mqtt_listen_function(client, userdata, msg):

    # retriev data from MQTT server
    data = json.loads(msg.payload)

    # make prediction and add it to data dictionary
    data['prediction'] = predict.predict(data['date'],
                                 data['ubication'],
                                 data['temperature'],
                                 data['humidity'],
                                 data['radiation'])

    # add actual date to data dictionary
    data['date'] = time.time()

    print data['date']
    print data['ubication']
    print data['temperature']
    print data['humidity']
    print data['radiation']
    print data['prediction'] 

    # open record file (where the samples are saved)
    my_file = Path("data/records.csv")
    if my_file.is_file():
        df = pd.read_csv('data/records.csv')
    else:
        df = pd.DataFrame(columns = ['date',
                                     'ubication',
                                     'temperature',
                                     'humidity',
                                     'radiation',
                                     'prediction'])

    # concatenate actual sample to prev csv
    df.loc[df.shape[0]] = [data['created_at'],
                           data['ubication'],
                           data['temperature'],
                           data['humidity'],
                           data['radiation'],
                           data['prediction']]

    #
    # Obtener la prediccion que se hizo para la radiacion actual
    # enviar los datos actuales con la prediccion que se hizo
    #

    # save df with new records
    df.to_csv('data/records.csv')

    # create dictionary to send to thingSpeak
    thingSpeakData = {
        'field1': data['created_at'],
        'field2': data['ubication'],
        'field3': data['temperature'],
        'field4': data['humidity'],
        'field5': data['radiation'],
        'field6': data['prediction'],
        'key': thingspeakKey
        }

    thingSpeakBridge.sendToThingSpeak(thingSpeakData)

    
if __name__ == "__main__":

    mqttClient.set_on_message(mqtt_listen_function)
    mqttClient.listenToBroker(brokerIp, brokerPort, topic)
    
