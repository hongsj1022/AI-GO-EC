import paho.mqtt.publish as publish

MQTT_HOST = "163.180.117.43"

publish.single(topic="/detect/cw", payload="1", hostname=MQTT_HOST)
publish.single(topic="/endinform/tts", payload="1", hostname=MQTT_HOST)

