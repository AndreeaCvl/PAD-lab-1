import requests
from flask import request, jsonify, Flask
from fav_db_test import FavDatabaseHandler

db_handler = FavDatabaseHandler()
app = Flask(__name__)


# Create a session with the default timeout
session = requests.Session()
session.timeout = 0.5


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "service": "favorites"}), 200


@app.route('/users/<user_id>/favorites/add', methods=['POST'])
def add_to_favorites(user_id):
    try:
        data = request.get_json()
        product_id = data.get('product_id')

        if product_id:
            db_handler.add_to_favorites(user_id, product_id)

            # Send a notification to products.py about the favorited product
            response = session.post(f"http://localhost:5001/product_to_favorite", json={"product_id": product_id})

            if response.status_code == 200:
                return jsonify({"message": f"Product {product_id} added to favorites for user {user_id}"}), 201
                print(" notified products service")

            else:
                print("Failed to notify products service")
                return jsonify({"error": "Failed to notify products service"}), 500

            #return jsonify({'message': f'Product {product_id} added to favorites for User ID {user_id}'}), 200
        else:
            return jsonify({'error': 'Product ID is required'}), 400

    except Exception as e:
        print('exception')
        return jsonify({'error': str(e)}), 500


@app.route('/users/<user_id>/favorites', methods=['GET'])
def see_favorites_by_user_id(user_id):
    favorites = db_handler.get_favorites_by_user_id(user_id)
    if favorites:
        formatted_favorites = ', '.join(favorites)
        return f'Favorites for User ID {user_id}: {formatted_favorites}'
    else:
        return f'The user with ID {user_id} has added no favorites yes'


if __name__ == '__main__':
    app.run(port=5000)


