import pika
from sys import argv
from os import getenv

# Connection params
host = getenv('RBMQ_HOST', 'localhost')
port = getenv('RBMQ_PORT', 5672)
vhost = getenv('RBMQ_VHOST', '/')
username = getenv('RBMQ_USERNAME', 'guest')
password = getenv('RBMQ_PASSWORD', 'guest')

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host, port, vhost, credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# Queue
qname = getenv('RBMQ_CHANNEL', 'test')

channel.queue_declare(qname)

message = " ".join(argv[1:]) or "some message"

channel.basic_publish(exchange='' , routing_key=qname, body=message)

# Close connection after done
connection.close()
