from lib.mqttClient import sendToBroker
from lib.sensors import readDHT

brokerIp = "192.168.1.135"
brokerPort = 1883
topic = "solar"

if __name__ == "__main__":
    payload = readDHT()
    print payload
    if sendToBroker(brokerIp, brokerPort, payload, topic):
        print "Successfully published in broker"
    else:
        print "Error publishing in broker"    
