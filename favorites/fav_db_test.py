import psycopg2

class FavDatabaseHandler:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="fav_test2",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )

    def see_users(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM users''')

        # Fetch all rows from the result set
        data = cur.fetchall()
        cur.close()

        formatted_data = "\n".join(
            [f"User ID: {user[0]}, Username: {user[1]}, Favorites: {user[2]}" for user in data])
        print(formatted_data)

        # Return the formatted data as plain text response
        return formatted_data

    def get_favorites_by_user_id(self, user_id):
        cur = self.conn.cursor()
        cur.execute('SELECT favs FROM users WHERE user_id = %s', (user_id,))
        favorites = cur.fetchone()
        cur.close()
        print(favorites)
        return favorites[0] if favorites else None

    def add_to_favorites(self, user_id, product_id):
        current_favorites = self.get_favorites_by_user_id(user_id)

        if current_favorites is not None:
            if product_id in current_favorites:
                pass
            else:
                current_favorites.append(product_id)
        else:
            current_favorites = [product_id]

        cur = self.conn.cursor()
        cur.execute('INSERT INTO users (user_id, favs) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET favs = %s',
                    (user_id, current_favorites, current_favorites))
        self.conn.commit()
        cur.close()

    def __del__(self):
        self.conn.close()
