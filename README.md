# TFG - Solar prediction

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3be38ff6640c402fa1a0b31df74852d5)](https://www.codacy.com/app/acoronado/TFG?utm_source=github.com&utm_medium=referral&utm_content=MrSlide22/TFG&utm_campaign=badger)

This project tries to predict the solar radiation based on **temperature, humidity and the actual solar radiation**.

The system is composed of two elements: the node and the server

## Node
### Prerequisites
#### HardWare
- **Raspberry Pi 2 model B** with a Linux distribution *(we use Raspbian)*
- 1 Led
- 1 [DHT22](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf) to measure temperature and humidity
- Piranometer *(we don't have it integrated in the project yet)*

*The wiring is described in [node/node_setup.txt](node/node_setup.txt)*

#### Software
In the Raspberry pi we need
- [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt/1.1): ```pip install paho-mqtt```

### Installation
- Place the folder **node** in our Raspberry Pi
- Change the variables brokerIp, brokerPort, topic, ubication in solar_node.py

### Usage
- Execute [node/solar_node.py](node/solar_node.py)

## Server
### Prerequisites
- [thingspeak](https://thingspeak.com/) account
- [Mosquitto](https://mosquitto.org/)

### Python version and libraries
- Python 2.7
- Pandas to manage csv files ```sudo pip install pandas```
- Paho MQTT to create the listener of the MQTT server ```sudo pip install paho-mqtt```

### Installation
- Place the folder **server** in your server.
- Change the variables brokerIp, brokerPort, topic and thingspeakKey in solar_node.py

### Usage
- execute ```mosquitto```
- execute [server/main.py](server/main.py)
