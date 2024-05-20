import sqlite3
import json
import os
from datetime import datetime
import csv
from io import TextIOWrapper
class User:
    def __init__(self, email, name, lastname, password, birthday=None,is_admin = 0):
        self.email = email
        self.name = name
        self.lastname = lastname
        self.password = password
        self.birthday = birthday
        self.is_admin = is_admin
        

    @staticmethod
    def calculate_days_to_birthday(birthday):
        if birthday is None:
            return None

        # Convert birthday to datetime object
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        # Get current date
        current_date = datetime.now().date()

        # Calculate days to birthday
        next_birthday = datetime(current_date.year, birthday_date.month, birthday_date.day).date()
        if next_birthday < current_date:
            next_birthday = datetime(current_date.year + 1, birthday_date.month, birthday_date.day).date()
        days_to_birthday = (next_birthday - current_date).days

        return days_to_birthday

    @staticmethod
    def connect_to_database(db_file):
        conn = sqlite3.connect(db_file)
        return conn

    def add_user(self, conn):
        try:
            c = conn.cursor()
            c.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)",
                      (self.email, self.name, self.lastname, self.password, self.birthday,self.is_admin))
            conn.commit()
            print("User added successfully.")
        except sqlite3.IntegrityError:
            print("Error: User already exists with this email.")

    @staticmethod
    def add_user_from_csv(conn, csv_file):
        try:
            csv_wrapper = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_wrapper)

            users_added = []
            next(csv_reader)
            for row in csv_reader:
                if len(row) != 6:  # Assuming each row has exactly 6 columns
                    continue
                email, name, lastname, password, is_admin, birthday = row
                user = User(email=email, name=name, lastname=lastname, password=password, birthday=birthday,is_admin = is_admin)
                if user.add_user(conn):
                    users_added.append(user)


            return f"{len(users_added)} user(s) added successfully."
        except Exception as e:
            return f"Error: {e}"

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
        conn = sqlite3.connect(os.path.abspath("") +'/database.db')
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
                    'birthday': user[3],
                    'left_to_birthday' : User.calculate_days_to_birthday(user[3]),
                })

        user_list_sorted = sorted(user_list, key=lambda x: x['left_to_birthday'])   

        return user_list_sorted


