import pika
from os import getenv
from os import _exit as os_exit
from sys import exit as sys_exit

def main():

    # Connection params
    #
    # If running from a docker compose, use the environment variables
    # given, otherwise, define them with the default values.
    host     : str = getenv('CUSTOM_HOSTNAME',    'localhost')
    port     : int = getenv('RABBITMQ_NODE_PORT',        5672)
    vhost    : str = getenv('RBMQ_VHOST',                 '/')
    username : str = getenv('RBMQ_USERNAME',          'guest')
    password : str = getenv('RBMQ_PASSWORD',          'guest')
    qname    : str = getenv('RBMQ_QUEUE',              'test')


    # Initialize
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, vhost, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(qname)


    # Logic
    def callback(ch, method, props, body: bytes) -> None:
        print(f">>> Received: '{body}'")

    channel.basic_consume(queue=qname, auto_ack=True, on_message_callback=callback)

    channel.start_consuming()


# Execute and graceful exit
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys_exit(0)
        except:
            os_exit(0)