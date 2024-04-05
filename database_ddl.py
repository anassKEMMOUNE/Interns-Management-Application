import sqlite3
import hashlib
# To run once on activation

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''DROP TABLE User''')
c.execute('''CREATE TABLE IF NOT EXISTS User (
                email TEXT PRIMARY KEY,
                name TEXT,
                lastname TEXT,
                password TEXT,
                is_admin INTEGER
            )''')
conn.commit()
conn.close()

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Hash the password
hashed_password = hashlib.sha256('admin'.encode()).hexdigest()

# Insert admin user into the User table
c.execute("INSERT INTO User (email, name, lastname, password, is_admin) VALUES (?, ?, ?, ?, ?)",
          ('admin@admin.com', 'admin', 'user', hashed_password,1))

# Commit changes and close connection
conn.commit()
conn.close()