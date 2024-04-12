from confluent_kafka import Consumer, KafkaException
import json
import mysql.connector
import os

def db_connect():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_SERVICE_HOST'),
        port=os.getenv('MYSQL_SERVICE_PORT'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

kafka_conf = {
    'bootstrap.servers': os.getenv('SIMPLE_KAFKA_SERVICE_HOST') + ':' + os.getenv('SIMPLE_KAFKA_SERVICE_PORT'),
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(**kafka_conf)

def consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            msg_value = json.loads(msg.value().decode('utf-8'))
            print(f"Received message: {msg_value}")
            process_message(msg_value)

    finally:
        consumer.close()

def process_message(message):
    db = db_connect()
    cursor = db.cursor()

    try:
        if message['action'] == 'POST':
            sql = "INSERT INTO products (id, name, description) VALUES (%s, %s, %s)"
            val = (message['data']['id'], message['data']['name'], message['data']['description'])
            cursor.execute(sql, val)
            db.commit()
        elif message['action'] == 'GET':
            pass

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    consume_loop(consumer, ['product_requests', 'product_additions'])
