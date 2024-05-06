import sqlite3
import json
class User:
    def __init__(self, email, name, lastname, password, is_admin, birthday=None):
        self.email = email
        self.name = name
        self.lastname = lastname
        self.password = password
        self.is_admin = is_admin
        self.birthday = birthday

    @staticmethod
    def connect_to_database(db_file):
        conn = sqlite3.connect(db_file)
        return conn

    def add_user(self, conn):
        try:
            c = conn.cursor()
            c.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)",
                      (self.email, self.name, self.lastname, self.password, self.is_admin, self.birthday))
            conn.commit()
            print("User added successfully.")
        except sqlite3.IntegrityError:
            print("Error: User already exists with this email.")

    @staticmethod
    def delete_user(conn, email):
        try:
            c = conn.cursor()
            c.execute("DELETE FROM User WHERE email=?", (email,))
            conn.commit()
            print("User deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting user:", e)

    @staticmethod
    def modify_user(conn, email, **kwargs):
        try:
            c = conn.cursor()
            update_query = "UPDATE User SET "
            values = []
            for key, value in kwargs.items():
                update_query += f"{key}=?, "
                values.append(value)
            update_query = update_query.rstrip(", ") + " WHERE email=?"
            values.append(email)
            c.execute(update_query, tuple(values))
            conn.commit()
            print("User modified successfully.")
        except sqlite3.Error as e:
            print("Error modifying user:", e)

    @staticmethod
    def get_user(conn, email):
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM User WHERE email=?", (email,))
            user_data = c.fetchone()
            if user_data:
                return User(*user_data)
            else:
                print("User not found.")
                return None
        except sqlite3.Error as e:
            print("Error fetching user:", e)

    @staticmethod
    def get_all_users(exclude_admin=True):
        """Retrieve all users from the database."""
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if exclude_admin:
            c.execute("SELECT email, name, lastname, birthday, is_admin FROM User WHERE email != 'admin@admin.com'")
        else:
            c.execute("SELECT email, name, lastname, birthday, is_admin FROM User")

        users = c.fetchall()
        print("useeers   ",users)
        conn.close()

        user_list = []
        for user in users:
            if user[0]!="admin@admin.com":
                user_list.append({
                    'email': user[0],
                    'name': user[1],
                    'lastname': user[2],
                    'birthday': user[4],
                })

        return user_list

