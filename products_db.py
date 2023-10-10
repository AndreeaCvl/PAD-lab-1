from datetime import datetime

import psycopg2

class ProductsDatabaseHandler:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="products",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )

    def create_table(self):
        cur = self.conn.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                product_name TEXT,
                productDescription TEXT,
                price DECIMAL,
                favorites INTEGER,
                time TIMESTAMP
            );
        '''

        # Execute the query
        cur.execute(create_table_query)

        # Commit the transaction and close the cursor and connection
        self.conn.commit()
        cur.close()

    def fetch_all_products(self):
        cur = self.conn.cursor()

        fetch_all_query = "SELECT * FROM products;"
        cur.execute(fetch_all_query)

        # Fetch all rows from the result set
        products = cur.fetchall()

        # Close the cursor
        cur.close()

        return products

    def add_product(self, product_id, user_id, product_name, product_description, price):
        cur = self.conn.cursor()

        current_time = datetime.now()

        add_product_query = '''
            INSERT INTO products (product_id, user_id, product_name, productDescription, price, favorites, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''

        product_data = (product_id, user_id, product_name, product_description, price, 0, current_time)

        # Execute the query with the product data
        cur.execute(add_product_query, product_data)

        # Commit the transaction and close the cursor
        self.conn.commit()
        cur.close()

    def delete_product_by_id(self, product_id):
        cur = self.conn.cursor()

        delete_product_query = "DELETE FROM products WHERE product_id = %s;"

        try:
            # Execute the query with the product_id as a parameter
            cur.execute(delete_product_query, (product_id,))

            # Commit the transaction
            self.conn.commit()

            # Check if any row was deleted
            if cur.rowcount == 0:
                return False  # Product with given ID not found
            else:
                return True  # Product deleted successfully

        except psycopg2.Error as e:
            print("Error deleting product:", e)
            return False  # Error occurred during deletion

        finally:
            # Close the cursor
            cur.close()

    def search_products_by_name(self, product_name):
        cur = self.conn.cursor()

        search_product_query = "SELECT * FROM products WHERE product_name ILIKE %s;"
        # ILIKE is used for case-insensitive search

        try:
            # Execute the query with the product_name as a parameter
            cur.execute(search_product_query, ('%' + product_name + '%',))

            # Fetch all rows from the result set
            products = cur.fetchall()

            return products

        except psycopg2.Error as e:
            print("Error searching for products:", e)
            return None  # Error occurred during search

        finally:
            # Close the cursor
            cur.close()

    def increase_favorites_counter(self, product_id):
        cur = self.conn.cursor()

        increase_favorites_query = '''
            UPDATE products 
            SET favorites = favorites + 1 
            WHERE product_id = %s;
        '''

        try:
            # Execute the query with the product_id as a parameter
            cur.execute(increase_favorites_query, (product_id,))

            # Commit the transaction
            self.conn.commit()

            # Check if any row was updated
            if cur.rowcount == 0:
                return False  # Product with given ID not found
            else:
                return True  # Favorites updated successfully

        except psycopg2.Error as e:
            print("Error increasing favorites:", e)
            return False  # Error occurred during update

        finally:
            # Close the cursor
            cur.close()


if __name__ == '__main__':
    a = ProductsDatabaseHandler()

    # a.add_product("1", "1", "eraser", "removes things", 10)
    # a.add_product("2", "1", "pen", "writes no remove", 10)
    # a.add_product("3", "3", "pencil", "grafit", 10)

    #a.delete_product("1")
    res = a.fetch_all_products()
    print(res)
    search = a.search_product_by_name("pen")
    print(search)



