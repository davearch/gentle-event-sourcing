from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify({"message": "Product found", "product_id": product_id}), 200

@app.route('/products', methods=['POST'])
def post_product():
    data = request.get_json()
    return jsonify({"message": "Product created", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

