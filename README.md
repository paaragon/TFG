# TFG - Solar prediction
This project tries to predict the solar radiation based on **temperature, humidity and the actual solar radiation**.
##Node
###Prerequisites
####HardWare
- **Raspberry Pi 2 model B** with a Linux distribution *(we use Raspbian)*
- 1 Led
- 1 [DHT22](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf) to measure temperature and humidity
- Piranometer *(we don't have it integrated in the project yet)*

*The wiring is described in [node/node_setup.txt](node/node_setup.txt)*

####Software
In the Raspberry pi we need
- [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt/1.1): ```pip install paho-mqtt```

###Installation
- Place the folder **node** in our Raspberry Pi

###Usage
- Change the variables brokerIp, brokerPort, topic, ubication in solar_node.py
- Execute [node/solar_node.py](node/solar_node.py)

##Server
###Prerequisites
-  [Mosquitto](https://mosquitto.org/)

###Installation
- Place the folder **server** in your server.

###Usage
- execute ```mosquitto```
- execute [server/main.py](server/main.py)