import uuid

import requests
from flask import request, jsonify, Flask
from products_db import ProductsDatabaseHandler


products_handler = ProductsDatabaseHandler()
app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    # You can add more details to the status response if needed
    return jsonify({"status": "ok", "service": "products"}), 200


@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    product_id = str(uuid.uuid4())  # Convert UUID object to string for storage
    user_id = data.get('user_id')
    product_name = data.get('product_name')
    product_description = data.get('product_description')
    price = data.get('price')

    products_handler.add_product(product_id, user_id, product_name, product_description, price)

    #return jsonify({"message": f"{product_id}"}), 201
    return product_id, 201


@app.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    deleted = products_handler.delete_product_by_id(product_id)

    if deleted:
        return jsonify({"message": f"Product with ID {product_id} deleted successfully"}), 200
    else:
        return jsonify({"error": f"Product with ID {product_id} not found or deletion failed"}), 404


@app.route('/products', methods=['GET'])
def search_products():
    product_name = request.args.get('name', default='', type=str)
    products = products_handler.search_products_by_name(product_name)

    if products is not None:
        return jsonify(products), 200
    else:
        return jsonify({"error": f"Error occurred while searching for products with name '{product_name}'"}), 500


@app.route('/products', methods=['GET'])
def search_all_products():
    products = products_handler.fetch_all_products()

    if products is not None:
        return jsonify(products), 200
    else:
        return jsonify({"error": f"Error occurred while fetching products"}), 500


@app.route('/product_to_favorite', methods=['POST'])
def handle_favorite_product():
    data = request.get_json()
    product_id = data.get('product_id')

    res = products_handler.increase_favorites_counter(product_id)

    if res:
        return jsonify({"message": f"Favorites count updated for product {product_id}"}), 200
    else:
        return jsonify({"message": f"Failed to add to fav product with id {product_id}"}), 500


if __name__ == '__main__':
    app.run(port=5001)


