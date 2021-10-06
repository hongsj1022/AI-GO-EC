import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from server.socket_capture import *
from car.main_engine import *
from trafficlight.detect_tl import tl_run
import json
from crosswalk.detect_cw import cw_run
import paho.mqtt.publish as publish
from collections import deque

def on_message(client, userdata, msg):
    global cw
    if (msg.topic == "/detect/cw"):
        cw = int(msg.payload.decode('utf-8'))
    print(msg.topic+" " +str(msg.payload))


def load_config(filename):
    cfg: dict
    with open(filename, 'r') as f:
        cfg = json.load(f)

    return cfg


if __name__ == '__main__':

    MQTT_HOST = "163.180.117.43"

    # Car detection config.
    cfg = load_config('/home/aigo/detect/car/config.json')
    me = MainEngine(cfg)

    socket_capture_l = BufferlessSocketCapture(9997)
    socket_capture_c = BufferlessSocketCapture(9998, isCenter=True)
    socket_capture_r = BufferlessSocketCapture(9999)

    isSafe = 0
    print('good')

    global cw
    cw = 0
    client = mqtt.Client()
    client.on_message = on_message

    client.connect("163.180.117.43")
    client.subscribe("/detect/cw",0)
    
    # If AI-GO arrived in front of crosswalk
    while (client.loop()==0):
        if(cw==1):
            cw = 0
            break

    # Crosswalk detection
    # cw_res == 1 : Crosswalk exists -> Detect Traffic Light
    # cw_res == -1 : No Crosswalk

    # Trafficlight detection
    # tl_res == 1 : Go
    # tl_res == -1 : No Traffic Light -> Detect Car


    while True:
        
        if socket_capture_c.isConnected() == True:
            print("connected")
            tl_res = tl_run()
            if tl_res == 1: # If Trafficlight detected
                publish.single(topic="/detect/tl", payload="1", hostname=MQTT_HOST)
                break
            elif tl_res == -1:  # If Trafficlight not detected
                # Car detection
                while True:
                    if socket_capture_l.isConnected() == True:
                        ret, img = socket_capture_l.read()
                        detections, distances = me.run(img)
                        min_distance = 100
                        for distance in distances:
                            if distance < min_distance:
                                min_distance = distance            
                        if min_distance < 10:
                            isSafe += 1
                        else:
                            isSafe = 0
                    if isSafe > 20:
                        publish.single(topic="/detect/car", payload="1", hostname=MQTT_HOST)
                        break
            else:
                pass
