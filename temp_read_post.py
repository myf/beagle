import requests
import json
import random
import time
import twiggy as tw
import serial

s = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

tw.quickSetup(file='pachube.log')
tw.log.info('starting pachube_post.py')

# authentication headers
headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}

def post_nimbits(value):
    nimbits_data = {"email":"drdrsoto@gmail.com",
               "secret":"01787ade-c6d6-4f9b-8b86-20850af010d9",
               "point":"603_Test_Stream",
               "value":value}

    r = requests.post("http://app.nimbits.com/service/currentvalue", data=nimbits_data)

def post_pachube(value):
    data={"version":"1.0.0","datastreams":[{"id":"01","current_value":value}]}
    try:
        resp=requests.put('http://api.pachube.com/v2/feeds/39985',headers=headers,data=json.dumps(data))
    except:
        tw.log.trace('error').warning('bad request')
    if resp.status_code == 200:
        tw.log.info('pachube response value = ' + str(resp.status_code))
    else:
        tw.log.error('pachube response value = ' + str(resp.status_code))

# sleep for a minute, send random number to pachube in json format
while 1:
    tw.log.info("top of loop")
    data_value = 0
    # read temperature from arduino
    serial_response = s.write(chr(0x00))
    tw.log.info("arduino write response = " + str(serial_response))
    time.sleep(0.5)
    serial_response = None
    try:
        serial_response=ord(s.read())
    except:
        tw.log.trace('error').warning('bad serial read from arduino')

    tw.log.info("arduino temp response = " + str(serial_response))

    if serial_response:
        data_value = serial_response / 1024.0 * 5 * 100

        post_nimbits(data_value)
        post_pachube(data_value)

    time.sleep(60)
