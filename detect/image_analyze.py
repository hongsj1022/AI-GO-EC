import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from car.socket_capture import *
from car.main_engine import *
from trafficlight.detect_tl import tl_run
import json
from crosswalk.detect_cw import cw_run
import paho.mqtt.publish as publish
from collections import deque
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    global cw, notl, tts
    if (msg.topic == "/detect/cw"):
        cw = int(msg.payload.decode('utf-8'))
    if (msg.topic == "/detect/notl"):
        notl = int(msg.payload.decode('utf-8'))
    if (msg.topic == "/endinform/tts"):
        tts = int(msg.payload.decode('utf-8'))

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
    print("Socket for left camera has opened!")
    socket_capture_c = BufferlessSocketCapture(9998, isCenter=True)
    print("Socket for center camera has opened!")
    #socket_capture_r = BufferlessSocketCapture(9999)
    #print("Socket for right camera has opened!")

    isSafe = 0

    global cw, notl, tts
    cw = notl = tts = 0
    client = mqtt.Client()
    client.on_message = on_message

    client.connect("163.180.117.43")
    client.subscribe("/detect/cw",0)
    client.subscribe("/endinform/tts",0)
    
    # Crosswalk detection
    # cw_res == 1 : Crosswalk exists -> Detect Traffic Light
    # cw_res == -1 : No Crosswalk

    # Trafficlight detection
    # tl_res == 1 : Go
    # tl_res == -1 : No Traffic Light -> Detect Car

    #target_pt = 123.45

    while True:
        '''
        if socket_capture_r.isConnected() == True:
            
            print("Connected to Right Camera")
            print("Start crosswalk detection")

            #Crosswalk detection
            
            1) Crosswalk detection and return the center point of detected crosswalk
            while True:
                cw_res, pt_res = cw_run()
                if cw_res == -1:
                    print("Crosswalk not detected!")
                    pass
                elif cw_res == 1:
                    if pt_res - target_pt <= 10:
                        publish.single(topic="/detect/cw", payload=angle, hostname=MQTT_HOST)
                        break
                else:
                    pass
         '''
        # If AI-GO arrived in front of crosswalk
        while (client.loop()==0):
            if(cw==1):
                cw = 0
                break

        if socket_capture_c.isConnected() == True:
            print("Connected to Center Camera")
            print("Start trafficlight detection")
            
            #Trafficlight detection
            tl_res = tl_run()
            if tl_res == 1: # If Trafficlight detected
                publish.single(topic="/detect/tl", payload="1", hostname=MQTT_HOST)
                break
            
            elif tl_res == -1:  # If Trafficlight not detected
                publish.single(topic="/detect/notl", payload="1", hostname=MQTT_HOST)
                print("Trafficlight not detected, Waiting for end of TTS")
                while (client.loop()==0):
                    if(tts==1):
                        tts = 0
                        break
                   
                # Car detection
                print("Start Car detection")
                while True:
                    if isSafe > 1000:
                        publish.single(topic="/detect/nocar", payload="1", hostname=MQTT_HOST)
                        isSafe =0
                        break
                    if socket_capture_l.isConnected() == True:
                        ret, img = socket_capture_l.read()

                        if ret:
                            detections, distances = me.detect(img)
                            min_distance = 100
                            if detections==None or distances==None:
                                print("None")
                                isSafe += 1
                                continue
                            for distance in distances:
                                if distance != 0 and distance < min_distance:
                                    #print(f'distance is {distance}')
                                    min_distance = distance
                            print(f'Closest car is in {min_distance}')
                            if min_distance > 35:
                                print("Car is faraway")
                                isSafe += 1
                            else:
                                print("Watch out! Car is coming!")
                                isSafe = 0
            else:
                pass
