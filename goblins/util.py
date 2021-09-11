from kombu import Connection, Exchange, Queue


ex = Exchange('goblins', 'topic')
q = Queue('action_commands', exchange=ex, routing_key='action_command')


def publish(data):
    with Connection(
        hostname='104.237.1.145/',
        userid='bruno',
        password='bruno',
        virtual_host='beelze') as con:
                producer = con.Producer(serializer='msgpack')
                producer.publish(
                    data,
                    exchange=ex,
                    routing_key='action_command', queue=[q]
                )
