# Name: read_sensor.py

import sys
import time
import connection
import pika
import os
import yaml
import json
import signal

# Read pi  cpu temp
def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (float(temp.replace("temp=", "").replace("'C", "")))

# Establish outgoing connection to cloud RabbitMQ
# Read config parameters for cloud RabbitMQ
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    cloud_hostname = config['cloud_hostname']
    cloud_username = config['cloud_username']
    cloud_password = config['cloud_password']
    cloud_port = config['cloud_port']
cloud_credentials = pika.PlainCredentials(cloud_username, cloud_password)

# Establish outgoing connection to edge RabbitMQ
# Read config parameters for edge RabbitMQ
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    edge_hostname = config['edge_hostname']
    edge_username = config['edge_username']
    edge_password = config['edge_password']
    edge_port = config['edge_port']
edge_credentials = pika.PlainCredentials(edge_username, edge_password)

# IMPORTANT: Sensor ID should be changed by each user of this script depending on their sensor
# (As of 03-30-18) Light: 1 / Vibration: 2 / Sound: 3 / Temp/Humidity: 4 / Ultrasonic: 5 / Tilt: 6
sensorID = 4

# This method submits sensor data with a unique sensor ID to RabbitMQ for processing
def publish_to_mq(temp, time_stamp):
    entry = {}
    entry['temp'] = temp
    entry['sensor_type'] = sensorID
    entry['time_stamp'] = time_stamp
    temp_to_send = json.dumps(entry)
    # Publish message to outgoing exchange
    cloud_channel.basic_publish(exchange='temp_from_pi',
                                routing_key='key_yellow',
                                body=temp_to_send)
    edge_channel.basic_publish(exchange='temp_from_pi',
                               routing_key='key_yellow',
                               body=temp_to_send)
    # Indicate delivery of message
    print(" [ >> ] Sent ", entry)
    time.sleep(0.01)

def close_pika(signal, frame):
    print('Closing Pika Connection')
    connection.close()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, close_pika)
    # Establish outgoing connection to Temp Queue
    cloud_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=cloud_hostname, credentials=cloud_credentials, port=cloud_port))
    cloud_channel = cloud_connection.channel()
    cloud_channel.exchange_declare(exchange='temp_from_pi', exchange_type='direct')
    edge_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=edge_hostname, credentials=edge_credentials, port=edge_port))
    edge_channel = edge_connection.channel()
    edge_channel.exchange_declare(exchange='temp_from_pi', exchange_type='direct')
    while True:
        temp = measure_temp()
        publish_to_mq(temp, time.strftime('%Y-%m-%d %H:%M:%S'))
        # Record data every 1 seconds
        time.sleep(1.0)
