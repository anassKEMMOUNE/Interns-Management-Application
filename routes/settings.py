from flask import render_template, request, redirect, url_for, session
import hashlib
from Models.user import User
import os

def settings_route(app) : 
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
                conn = User.connect_to_database(os.path.abspath("") +'/database.db')
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

                conn = User.connect_to_database(os.path.abspath("") +'/database.db')
                existing_user = User.get_user(conn, email)
                if existing_user:
                    return render_template('settings.html', error1='User already exists with this email.')

                new_user = User(email, name, lastname, password, birthday,is_admin)
                new_user.add_user(conn)

                return redirect(url_for('index'))
            elif action == 'add_multi_users' : 
                try:
                    csv_file = request.files['csv_file']
                    if not csv_file:
                        return "No CSV file uploaded."
                    conn = User.connect_to_database(os.path.abspath("") +'/database.db')
                    result = User.add_user_from_csv(conn, csv_file)
                    return render_template( "settings.html" ,message = result)
                except Exception as e:
                    return f"Error: {e}"


                    
                except Exception as e:
                    return f"Error: {e}"

        return render_template('settings.html')