import httplib
import urllib
import time


def sendToThingSpeak(data):

    headers = {"Content-typZZe": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    params = urllib.urlencode(data)
    conn = httplib.HTTPConnection("api.thingspeak.com:80")

    try:

        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()

        print response.status, response.reason

        data = response.read()

        print data

        conn.close()

    except:
        print "connection failed"


if __name__ == "__main__":

    from random import randint
    for i in range(0, 30):
        data = {'field4': randint(0, 500), 'key': 'O2M7W8NYQL5X7XD3'}
        sendToThingSpeak(data)
        time.sleep(16)
