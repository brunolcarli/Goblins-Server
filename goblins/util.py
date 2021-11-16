from kombu import Connection, Exchange, Queue
import paho.mqtt.client as mqtt #import the client1
import msgpack

ex = Exchange('goblins', 'topic')
q = Queue('action_commands', exchange=ex, routing_key='action_command')


# def publish(data):
#     with Connection(
#         hostname='104.237.1.145/',
#         userid='bruno',
#         password='bruno',
#         virtual_host='beelze') as con:
#                 producer = con.Producer(serializer='msgpack')
#                 producer.publish(
#                     data,
#                     exchange=ex,
#                     routing_key='action_command', queue=[q]
#                 )

def publish(data):
    broker_address="localhost"
    client = mqtt.Client("Server") #create new instancek
    print("connecting to broker")
    client.connect(broker_address, port=18883) #connect to broker
    client.loop_start() #start the loop
    # client.subscribe("house/bulbs/bulb1")
    # print("Publishing message to topic","house/bulbs/bulb1")
    data = msgpack.packb(data)
    print(data)
    client.publish("foo/baz", data)
    client.loop_stop() #stop the loop
