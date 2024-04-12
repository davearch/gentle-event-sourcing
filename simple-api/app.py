from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
import os

app = Flask(__name__)

kafka_conf = {
    'bootstrap.servers': os.getenv('SIMPLE_KAFKA_SERVICE_HOST') + ':' + os.getenv('SIMPLE_KAFKA_SERVICE_PORT'),
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'user1',
    'sasl.password': 'rQGpBE1VxJ',
    'client.id': 'flask-kafka-producer'
}

producer = Producer(**kafka_conf)


def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message produced: {msg.topic()} {str(msg.value())}")


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    producer.produce(
        'product_requests',
        key=str(product_id),
        value=json.dumps({"action": "GET", "product_id": product_id}),
        callback=acked
    )
    producer.poll(0)
    return jsonify({"message": "Product found", "product_id": product_id}), 200


@app.route('/products', methods=['POST'])
def post_product():
    data = request.get_json()
    producer.produce(
        'product_additions',
        key=str(data.get('id', '')),
        value=json.dumps({"action": "POST", "data": data}),
        callback=acked
    )
    producer.poll(0)
    return jsonify({"message": "Product created", "data": data}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

