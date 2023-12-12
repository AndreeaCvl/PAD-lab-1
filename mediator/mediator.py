import requests
import psycopg2
from flask import request, jsonify, Flask
import traceback


app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "service": "mediator"}), 200


@app.route('/mediator/<user_id>/favorites/add', methods=['POST'])
def add_to_favorites(user_id):
    try:
        data = request.get_json()
        product_id = data.get('product_id')

        print(product_id)

        # Connect to the first database (User Favorites)
        conn_user_favorites = psycopg2.connect(database="fav_test2",
                                              user="postgres",
                                              password="admin",
                                              host="localhost",
                                              port="5432")
        cursor_user_favorites = conn_user_favorites.cursor()

        # Connect to the second database (products)
        conn_products = psycopg2.connect(database="products",
                                        user="postgres",
                                        password="admin",
                                        host="localhost",
                                        port="5432")
        cursor_products = conn_products.cursor()

        try:
            # Start transactions
            conn_user_favorites.tpc_begin(conn_user_favorites.xid(42, 'transaction_ID_user', 'branch_qualifier_user'))
            conn_products.tpc_begin(conn_products.xid(42, 'transaction_ID_client', 'branch_qualifier_client'))

            cursor_user_favorites.execute("SELECT favs FROM users WHERE user_id = %s", (user_id,))
            existing_favs = cursor_user_favorites.fetchone()
            existing_favs = existing_favs[0] if existing_favs else None
            print(existing_favs)

            if existing_favs is not None:
                if product_id in existing_favs:
                    pass
                else:
                    existing_favs.append(product_id)
            else:
                existing_favs = [product_id]

            # Step 1: Add product to user favorites
            cursor_user_favorites.execute('INSERT INTO users (user_id, favs) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET favs = %s',
                    (user_id, existing_favs, existing_favs))
            # Step 2: Increase the number of client favorites
            cursor_products.execute("UPDATE products SET favorites = favorites + 1  WHERE product_id = %s;", (product_id,))

            # If everything is successful, commit the transactions
            conn_user_favorites.tpc_prepare()
            conn_products.tpc_prepare()

            # If both transactions are prepared, commit them
            conn_user_favorites.tpc_commit()
            conn_products.tpc_commit()

            print("added do db")
            return jsonify({"message": f"added it to db: {product_id}"}), 200

        except psycopg2.Error as e:
            # If an error occurs, roll back both transactions
            conn_user_favorites.tpc_rollback()
            conn_products.tpc_rollback()

            print("Database Error 1")
            traceback.print_exc()

            return jsonify({"message": f"Database Error: {e}"}), 500
            # Handle the error appropriately, e.g., return an error response to the client

        except Exception as e:
            # If an unexpected error occurs, roll back both transactions
            conn_user_favorites.tpc_rollback()
            conn_products.tpc_rollback()

            print("Database Error 2")
            #traceback.print_exc()

            return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
            # Handle the error appropriately, e.g., return an error response to the client

        finally:
            # Close the database connections
            conn_user_favorites.close()
            conn_products.close()

    except Exception as e:
        #traceback.print_exc()
        print("Database Error 3")
        return jsonify({"message": f"An unexpected error occurred outside the try-except block: {e}"}), 500
    # Handle the error appropriately, e.g., return an error response to the client


if __name__ == '__main__':
    app.run(port=5005)


