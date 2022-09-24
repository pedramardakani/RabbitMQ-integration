import pika
from sys import argv
from os import getenv

# Connection params
#
# If running from a docker compose, use the environment variables
# given, otherwise, define them with the default values.
host: str = getenv('CUSTOM_HOSTNAME', 'localhost')
port: int = getenv('RABBITMQ_NODE_PORT', 5672)
vhost: str = getenv('RBMQ_VHOST', '/')
qname: str = getenv('RBMQ_QUEUE', 'test')
e_name: str = getenv('RBMQ_LOGS', 'logs')
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

    # Exchange, send logs to everyone
    channel.exchange_declare(exchange=e_name, exchange_type='fanout')

    message = " ".join(argv[1:]) or "some message"

    channel.basic_publish(exchange=e_name , routing_key='', body=message)

    print('>>> Message sent 📨')

    connection.close()


# Execute and graceful exit
if __name__ == '__main__':

    connection = create_connection()

    try:
        main(connection)
    except KeyboardInterrupt:
        print('\nWARNING: interrupted ⛔\n')
        connection.close()
        try:
            sys_exit(0)
        except:
            os_exit(0)
