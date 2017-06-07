from lib.mqttClient import sendToBroker
from lib.sensors import readDHT
from lib.sensors import readDyn
import time
from time import localtime, strftime
import sys
import os
import json
import threading

#brokerIp = "192.168.1.135"
brokerIp = "solarcasting.dacya.ucm.es"
brokerPort = 1883
topic = "solar"
ubication = 1


def logData(data):
    csv = ""
    csv += str(data['ubication']) + ','
    csv += str(data['time']) + ','
    csv += str(data['temperature']) + ','
    csv += str(data['humidity']) + ','
    csv += str(data['radiation']) + ','
    csv += '\n'

    if not os.path.isdir('logs'):
        os.makedirs('logs')

    pathName = "log-" + strftime("%d%B%Y") + ".csv"
    with open("logs/" + pathName, "a") as log:
        log.write(csv)
        log.close()


def sendData(data):
    payload = json.dumps(data)

    state = sendToBroker(brokerIp, brokerPort, payload, topic)
    time = strftime("%d-%m-%Y %H:%M:%S", localtime())

    if state:
        message = time + " | success"
    else:
        message = time + " | failure"

    print message

    if not os.path.isdir('logs/mqtt'):
        os.makedirs('logs/mqtt')

    pathName = "mqttLog" + strftime("%d%B%Y") + ".csv"
    with open("logs/mqtt/" + pathName, "a") as log:
        log.write(time + "," + message)
        log.close()


def getData():
    data = dict()
    data['ubication'] = ubication
    data['time'] = strftime("%d-%m-%Y %H:%M:%S", localtime())
    data['temperature'], data['humidity'] = readDHT()
    data['radiation'] = readDyn()
    return data


def test():
    data = getData()
    print data
    sendData(data)


def start(interval, mode):
    
    print "Waiting till new minute comes..."
    secs = int(strftime("%S"))
    while ((secs % 10) != 0):
        secs = int(strftime("%S"))
    print "Starting."

    while True:
        data = getData()
        print "Data retrieved"
        logData(data)
        if mode == 1:
            t = threading.Thread(target=sendData, args=(data, ))
            t.start()
        time.sleep(interval-2)
  	secs = int(strftime("%S"))
    	while ((secs % 10) != 0):
        	secs = int(strftime("%S"))


def help():
    print "\nsudo python solar_node.py [start|test|help] [m|l] [i]"
    print "\nIf not command is specified, the program will take one single sample and save it into a log file."
    print "\n\t- start: turn on the client and collect samples. If nothing is specified, the interval time will be 5 minutes and the samples will be recorded into a log file."
    print "\t- test: collect one single sample and print the results. This command is intended to test wether the sensors are right connected or not."
    print "\n\tIf start command is selected,the data can be stored into a log file or send it to an mqtt server. The interval between samples can be modified"
    print "\t- m: the data will be send to an mqtt server"
    print "\t- l: (default option) the data will be stored into a log file"
    print "\t- i: specified the interval in seconds between taking one sample and another"


if __name__ == "__main__":

    if len(sys.argv) > 1:

        if sys.argv[1] == 'start':

            mode = 0

            if len(sys.argv) > 2 and sys.argv[2] == 'm':
                mode = 1

            start(60, mode)

        elif sys.argv[1] == 'test':
            test()

        elif sys.argv[1] == 'help':
            help()
        else:
            help()

    else:
        data = getData()
        logData(data)
