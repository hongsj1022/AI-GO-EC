import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from server.socket_capture import *
from car.main_engine import *
from trafficlight.detect_tl import tl_run
import json
from crosswalk.detect_cw import cw_run
import paho.mqtt.publish as publish


def load_config(filename):
    cfg: dict
    with open(filename, 'r') as f:
        cfg = json.load(f)

    return cfg


if __name__ == '__main__':

    MQTT_HOST = "210.114.91.98"

    # Car detection config.
    cfg = load_config('car/config.json')
    me = MainEngine(cfg)

    socket_capture_l = BufferlessSocketCapture(9997)
    socket_capture_c = BufferlessSocketCapture(9998)
    socket_capture_r = BufferlessSocketCapture(9999)

    # Crosswalk detection
    # cw_res == 1 : Crosswalk exists -> Detect Traffic Light
    # cw_res == -1 : No Crosswalk
    cw_res = cw_run()
    if cw_res == 1:     # If Crosswalk detected
        publish.single(topic="/detect/cw", payload="1", hostname=MQTT_HOST)

        # Trafficlight detection
        # tl_res == 1 : Go
        # tl_res == -1 : No Traffic Light -> Detect Car
        tl_res = tl_run()
        if tl_res == 1: # If Trafficlight detected
            publish.single(topic="/detect/tl", payload="1", hostname=MQTT_HOST)
        elif tl_res == -1:  # If Trafficlight not detected
            # Car detection
            while True:
                if socket_capture_r.isConnected() == True:
                    ret, img = socket_capture_r.read()
                    me.run(img)
        else:
            pass
    else:
        pass
