from flask import Flask, render_template, request, redirect, url_for, session,Response,send_from_directory
from Models.user import User
import hashlib
from utils.save_files import save_files
import os
def login_route(app) :
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        save_files([])
        if "email" in session :
            del session["email"]
            del session["admin"]

        if "keywords" in session :
            del session["keywords"]
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            conn = User.connect_to_database(os.path.abspath("") +'/database.db')
            user = User.get_user(conn, email)
            print("ana useeer ",user.birthday)
            
            if user:

                # Hash the provided password and compare with the stored hashed password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                if hashed_password == user.password :
                    # Login successful, set session
                    session['email'] = email
                    session['name'] = user.name
                    session['admin'] = user.is_admin
                    print("session admin : ",session["admin"])
                    return redirect(url_for('index'))
                else:
                    # Incorrect password
                    return render_template('login.html', error='Incorrect email or password.')
            else:
                # User not found
                return render_template('login.html', error='User not found.')

        return render_template('login.html')