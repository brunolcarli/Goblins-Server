import json
import paho.mqtt.client as mqtt
from django.conf import settings

def publish(data, topic):
    """
    Publish data to a MQTT topic.
    """
    broker_address = settings.MQTT['host']
    client = mqtt.Client(settings.MQTT['user'])
    client.connect(broker_address, port=int(settings.MQTT['port']))
    client.loop_start()

    client.publish(topic, json.dumps(data))
    client.loop_stop()
