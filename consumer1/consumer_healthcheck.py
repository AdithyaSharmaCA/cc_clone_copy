# health_check_microservice.py
import time
import pika
import mysql.connector
import logging

time.sleep(30)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='health2C2')
channel.queue_declare(queue='health2C3')
channel.queue_declare(queue='health2C4')
channel.queue_declare(queue='response')


logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body):
    print("Received response from Consumer2:", body.decode())
    logging.info(body.decode())
    if body.decode('utf-8') == "Yeah":
        logging.info("Consumer2 is healthy. !!!!!!")
        print("Consumer2 is healthy. !!!!!!")
    else:
        logging.info("Consumer2 is not healthy.     :(    ")
        print("Consumer2 is not healthy.     :(    ")

def check_health1():
    channel.basic_publish(exchange='', routing_key='health2C2', body="U running C1 ? ")
    # channel.basic_consume(queue='heath2C2', auto_ack=True)
    
    channel.basic_consume(queue='response', on_message_callback=callback, auto_ack=True)

    # Wait for a response from Consumer2 with a timeout
    timeout = 1  # Timeout in seconds
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            print("Timed out waiting for response from Consumer2. Consumer2 is not healthy.")
            logging.info("Timed out waiting for response from Consumer2. Consumer2 is not healthy.")
            break
        connection.process_data_events(time_limit=1)  # Process events for 1 second
        time.sleep(0.1)  # Sleep for a short duration to avoid busy-waiting



def check_health2():
    try:
        # Check RabbitMQ connection
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        connection.close()
        logging.info("RabbitMQ is healthy.")

        # Check MySQL connection
        cnx = mysql.connector.connect(user='root', password='Adithya@123', host='mysql', database='cc_project')
        cursor = cnx.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()
        cursor.close()
        cnx.close()
        logging.info("MySQL is healthy.")
    except pika.exceptions.AMQPConnectionError as rabbitmq_error:
        logging.info("RabbitMQ is UNHEALTHY :( !!!")
        print("RabbitMQ Error:", rabbitmq_error)
    except mysql.connector.Error as mysql_error:
        logging.info("MySQL is UNHEALTHY :( !!!")
        print("MySQL Error:", mysql_error)

while True:
    check_health1()
    check_health2()
    time.sleep(60)  # Check health every 60 seconds
