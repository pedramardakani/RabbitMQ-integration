import pika
from os import getenv
from time import sleep
from os import _exit as os_exit
from sys import exit as sys_exit

# Connection params
#
# If running from a docker compose, use the environment variables
# given, otherwise, define them with the default values.
host: str = getenv('CUSTOM_HOSTNAME', 'localhost')
port: int = getenv('RABBITMQ_NODE_PORT', 5672)
vhost: str = getenv('RBMQ_VHOST', '/')
qname: str = getenv('RBMQ_QUEUE', 'test')
username: str = getenv('RBMQ_USERNAME', 'guest')
password: str = getenv('RBMQ_PASSWORD', 'guest')


def create_connection() -> pika.BlockingConnection:

    # Initialize
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, vhost, credentials)
    connection = pika.BlockingConnection(parameters)

    return connection


def main(connection: pika.BlockingConnection):

    channel = connection.channel()

    # Give RabbitMQ a hint for a fair dispatch
    channel.basic_qos(prefetch_count=1)

    # Logic
    def callback(channel: pika.channel.Channel,
                 method: pika.spec.Basic.Deliver,
                 properties: pika.spec.BasicProperties,
                 body: bytes) -> str:
        print(f">>> ๐จ Received  '{body}' ")
        sleep(body.count(b'.'))
        print(f">>> โ Done with '{body}'")

        # Send manual acknowledgement
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.queue_declare(qname)

    # Set manual acknowledgement
    channel.basic_consume(queue=qname, auto_ack=False,
                          on_message_callback=callback)

    print(">>> Waiting for messages ๐คน Press CTRL+C to exit โ")
    channel.start_consuming()


# Execute and graceful exit
if __name__ == '__main__':

    connection = create_connection()

    try:
        main(connection)
    except KeyboardInterrupt:
        print('\nWARNING: interrupted โ\n')
        connection.close()
        try:
            sys_exit(0)
        except:
            os_exit(0)
