# How to install the node

## 1 - Requisites
- Raspberry Pi 2, 2 B+ or 3 with [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
- Internet connection
- [DHT22](https://www.adafruit.com/product/385)
- [MCP3008](https://www.adafruit.com/product/856)
- Pyranometer
- Enable SPI on raspbery with raspi-config

## 2 - Files

Copy this folder into the raspberry

## 3 - Wiring:
 
![Node wiring schema](readme_assets/solar_project_node_diagram.png)

## 4 - Dependencies

- Update
```
sudo apt-get update
sudo apt-get upgrade
```

- Python2.7
```
sudo apt-get install python2.7 build-essential python-pip python-dev
```

- Paho Mqtt: `pip install paho-mqtt`

- WiringPi: `pip install wiringpi2`

- Adafruit_DHT:
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
```

- Adafruit_GPIO:
```
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
```

- Adafruit_MCP3008:
```
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008
sudo python setup.py install
```
