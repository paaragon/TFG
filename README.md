# TFG - Solar prediction
This project tries to predict the solar radiation based on **temperature, humidity and the actual solar radiation**.
##Prerequisites
We need to build the node with the following components
- **Raspberry Pi 2 model B** with a Linux distribution *(we use Raspbian)*
- 1 Led
- 1 [DHT22](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf) to measure temperature and humidity
- Piranometer *(we don't have it integrated in the project yet)*

*The wiring is described in [node/node_setup.txt](node/node_setup.txt)*

##Installation
###Node
- Place the folder node in our Raspberry Pi

###Server
- Install [Mosquitto](https://mosquitto.org/).
- Place the server folder in your server.

##Usage
###Node
- Change the variables brokerIp, brokerPort, topic, ubication in solar_node.py
- Execute [node/solar_node.py](node/solar_node.py)

###Server
- execute mosquitto
- execute [server/main.py](server/main.py)
