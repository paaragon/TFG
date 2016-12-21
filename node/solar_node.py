from lib.mqttClient import sendToBroker
from lib.sensors import readDHT
from lib import fake_radiation as fk
import json

brokerIp = "192.168.1.135"
brokerPort = 1883
topic = "solar"
ubication = 1

if __name__ == "__main__":
    data = dict()
    data['ubication'] = ubication
    data['radiation'] = fk.getRadiation()
    data['temperature'], data['humidity'] = readDHT()
    payload = json.dumps(data)
    if sendToBroker(brokerIp, brokerPort, payload, topic):
        print "Successfully published in broker"
    else:
        print "Error publishing in broker"    
