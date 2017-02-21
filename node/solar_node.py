from lib.mqttClient import sendToBroker
from lib.sensors import readDHT
from lib import fake_radiation as fk
import json
import time

brokerIp = "192.168.1.135"
brokerPort = 1883
topic = "solar"
ubication = 1
interval = 30

def getData(): 
    data = dict()
    data['ubication'] = ubication
    data['radiation'] = fk.getRadiation()
    data['temperature'], data['humidity'] = readDHT()
    return data
    

def send():

    payload =json.dumps(getData())

    if sendToBroker(brokerIp, brokerPort, payload, topic):
        print "Successfully published in broker"
    else:
        print "Error publishing in broker"

def config():
    global brokerIp
    global brokerPort
    global topic
    global ubication
    global interval

    brokerIp = raw_input("MQTT broker Ip: ")
    brokerPort = int(raw_input("MQTT broker port: "))
    topic = raw_input("MQTT topic: ")
    ubication = int(raw_input("Ubication id: "))
    interval = int(raw_input("Interval (seconds): "))

def start():

    print "\nPress ctrl + C to stop"

    try:
        while True:
            send()
            time.sleep(interval)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    
    while(True):
        print "\nCommands: "
        print "1 - config"
        print "2 - send"
        print "3 - start"
        print "4 - exit\n"

        options = {'1': config,
                   '2': send,
                   '3': start,
                   '4': exit}
    
        command = raw_input("Enter a command number: ")

        if command == '4':
            break

        options[command]()
