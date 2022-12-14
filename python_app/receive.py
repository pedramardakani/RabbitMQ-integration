import pika
from os import getenv
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

    # Logic
    def callback(channel: pika.channel.Channel,
                 method: pika.spec.Basic.Deliver,
                 properties: pika.spec.BasicProperties,
                 body: bytes) -> str:
        print(f">>> ๐จ Received  '{body}' ")

    channel.queue_declare(qname)
    channel.basic_consume(queue=qname, auto_ack=True,
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
