from flask import Flask, render_template, request, redirect, url_for, session,Response
import sqlite3
import hashlib
from Models.user import User
import os
import CVfilter.extraction 
from CVfilter.Filtering import filterAll
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def save_files(files):
    # Define the directory to save the files
    upload_directory = os.path.join(app.root_path, 'Resumes')

    # Empty the directory
    for file_name in os.listdir(upload_directory):
        file_path = os.path.join(upload_directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # Save new files
    for file in files:
        file.save(os.path.join(upload_directory, file.filename))


@app.route('/')
def index():
    if "email" not in session :
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    save_files([])
    if "email" in session :
        del session["email"]

    if "keywords" in session :
        del session["keywords"]
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = User.connect_to_database("database.db")
        user = User.get_user(conn, email)
        
        if user:

            # Hash the provided password and compare with the stored hashed password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == user.password :
                # Login successful, set session
                session['email'] = email
                return redirect(url_for('index'))
            else:
                # Incorrect password
                return render_template('login.html', error='Incorrect email or password.')
        else:
            # User not found
            return render_template('login.html', error='User not found.')

    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if "email" not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form['action']  # Get the action from the form

        if action == 'change_password':
            old_password = request.form['oldpassword']
            new_password = request.form['newpassword']
            confirm_password = request.form['confirmpassword']

            hashed_old = hashlib.sha256(old_password.encode()).hexdigest()
            conn = User.connect_to_database("database.db")
            user = User.get_user(conn,session["email"])

            if hashed_old == user.password :
                if new_password == confirm_password :
                    hashed_new = hashlib.sha256(new_password.encode()).hexdigest()
                    User.modify_user(conn,session["email"],password = hashed_new)
                    return redirect(url_for('login'))
                else :
                    return render_template("settings.html",error = "password not matching")

            else :
                return render_template("settings.html", error = "wrong old password")

        elif action == 'add_user':
            email = request.form['email']
            name = request.form['name']
            lastname = request.form['lastname']
            password = request.form['password']
            password = hashlib.sha256(password.encode()).hexdigest()
            is_admin = request.form.get('is_admin') == 'on'  
            birthday = request.form.get('birthday')

            conn = User.connect_to_database("database.db")
            existing_user = User.get_user(conn, email)
            if existing_user:
                return render_template('settings.html', error1='User already exists with this email.')

            new_user = User(email, name, lastname, password, is_admin, birthday=birthday)
            new_user.add_user(conn)

            return redirect(url_for('index'))

    return render_template('settings.html')



@app.route('/cvfilter')
def cvfilter():
    if "email" not in session :
        return redirect(url_for('login'))
    filtered_resumes =  []
    if len(os.listdir('Resumes'))>0:
        keywords = session.get('keywords', [])
        filtered_resumes =  filterAll('Resumes',keywords)

    return render_template('cvfilter.html',files = filtered_resumes)



@app.route('/upload', methods=['POST'])
def upload():
    if "email" not in session :
        return redirect(url_for('login'))
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')

    if len(files) == 0:
        return redirect(request.url)

    try:
        save_files(files)
        keywords = request.form.getlist('keywords[]')
        session['keywords'] = keywords
        return redirect(url_for("cvfilter"))

    except Exception as e:
        return f"An error occurred: {str(e)}"
    


@app.route('/emails')
def emails():
    if "email" not in session:
        return redirect(url_for('login'))

    try:
        # Retrieve all users excluding the admin user
        user_data = User.get_all_users(exclude_admin=True)

        # Pass user data to the template
        print(user_data)
        return render_template("emails.html", users=user_data)


    except Exception as e:
        return render_template("error.html", error=str(e))

import json

@app.route('/calendar')
def calendars():
    if "email" not in session:
        return redirect(url_for('login'))

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Query all entries from the Calendar table
        c.execute("SELECT * FROM Calendar")
        entries = c.fetchall()

        # Close connection
        conn.close()

        # Convert entries to a dictionary with date as key
        calendar_data = {}
        for entry in entries:
            date = entry[0]
            if date not in calendar_data:
                calendar_data[date] = []
            calendar_data[date].append({
                'title': entry[1],
                'description': entry[2]
            })

        # Save calendar data to a JSON file
        with open('static/json/calendar_data.json', 'w') as json_file:
            json.dump(calendar_data, json_file)

        # Render the template
        return render_template("calendar.html")

    except Exception as e:
        return render_template("error.html", error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
