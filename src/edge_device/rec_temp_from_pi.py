# Name: simple_receive.py

# This program serves as a simple consumer script
# that allows messages to be received from RabbitMQ
# via a direct exchange
#
# NOTE: Execute on Raspberry Pi (before running
# simple_receive_and_send.py)

import pika
import sys
import MySQLdb
import datetime
import yaml
import json
import mysql.connector

# Read config parameters for mysql
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    host = config['mysql_hostname']
    username = config['mysql_username']
    password = config['mysql_password']
    database = config['mysql_database']
    port = config['mysql_port']

# Connect to mysql database and get cursor
mydb = mysql.connector.connect(
    host=host,
    user=username,
    passwd=password,
    database=database,
    port=port
)
mycursor = mydb.cursor()
mydb.commit()

# Read config parameters for RabbitMQ
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    hostname = config['hostname']
    username = config['username']
    password = config['password']
    port = config['port']
credentials = pika.PlainCredentials(username, password)


# Receive messages from temp sensor
def callback(ch, method, properties, body):
    # Receive temp
    temp = json.loads(body.decode('utf-8'))
    print(temp)
    # Save temp into mysql
    sql = "INSERT INTO temps_found (temp, sensor_type,  time_stamp) VALUES (%s, %s, %s)"
    val = (temp['temp'], temp['sensor_type'], temp['time_stamp'])
    mycursor.execute(sql, val)
    mydb.commit()

if __name__ == '__main__':
    # Establish incoming connection from temp sensor
    connection_in = pika.BlockingConnection(
        pika.ConnectionParameters(host=hostname, credentials=credentials, port=port))
    channel_in = connection_in.channel()
    channel_in.exchange_declare(exchange='temp_from_pi', exchange_type='direct')
    result_in = channel_in.queue_declare(exclusive=True)
    queue_in_name = result_in.method.queue
    channel_in.queue_bind(exchange='temp_from_pi', queue=queue_in_name, routing_key='key_yellow')

    # Indicate queue readiness
    print(' [*] Waiting for messages. To exit, press CTRL+C')

    # Consumption configuration
    channel_in.basic_consume(callback, queue=queue_in_name, no_ack=False)

    # Begin consuming from temp sensor
    channel_in.start_consuming()
