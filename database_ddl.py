import sqlite3
import hashlib

# To run once on activation

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Drop existing User table if it exists
c.execute('''DROP TABLE IF EXISTS User''')

# Create User table with the new birthday field
c.execute('''CREATE TABLE IF NOT EXISTS User (
                email TEXT PRIMARY KEY,
                name TEXT,
                lastname TEXT,
                password TEXT,
                birthday DATE,
                is_admin INTEGER
            )''')

# Commit changes and close connection
conn.commit()
conn.close()

# Connect to database again to insert initial admin user
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Hash the password
hashed_password = hashlib.sha256('admin'.encode()).hexdigest()

# Insert admin user into the User table
c.execute("INSERT INTO User (email, name, lastname, password, birthday, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
          ('admin@admin.com', 'admin', 'user', hashed_password, None, 1))

# Commit changes and close connection
conn.commit()
conn.close()

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Drop existing Calendar table if it exists
c.execute('''DROP TABLE IF EXISTS Calendar''')

# Create Calendar table with date as primary key
c.execute('''CREATE TABLE IF NOT EXISTS Calendar (
                date_ DATE ,
                title TEXT,
                description TEXT
            )''')

# Sample entries for demonstration
sample_entries = [
    ('2024-05-05', 'Meeting', 'Discuss project timeline'),
    ('2024-05-06', 'Work Party', 'Celebrate work party')
]

# Insert sample entries into the Calendar table
c.executemany("INSERT INTO Calendar (date_, title, description) VALUES (?, ?, ?)", sample_entries)

# Commit changes and close connection
conn.commit()
conn.close()
