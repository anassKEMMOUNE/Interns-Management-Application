from flask import Flask, render_template, request, redirect, url_for, session,Response
import sqlite3
import hashlib
from Models.user import User
import os
import CVfilter.extraction 
from CVfilter.Filtering import filterAll

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
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    save_files([])
    if "email" in session :
        del session["email"]
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
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        password = request.form['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        is_admin = request.form.get('is_admin') == 'on'  # Checkbox handling
        print(is_admin," is_admin")
        conn = User.connect_to_database("database.db")
        # Check if the user already exists
        existing_user = User.get_user(conn, email)
        if existing_user:
            return render_template('settings.html', error='User already exists with this email.')

        # Create a new user object and add it to the database
        new_user = User(email, name, lastname, password, is_admin)
        new_user.add_user(conn)

        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/cvfilter')
def cvfilter():
    filtered_resumes =  []
    if len(os.listdir('Resumes'))>0:
        keywords = session.get('keywords', [])
        filtered_resumes =  filterAll('Resumes',keywords)

    return render_template('cvfilter.html',files = filtered_resumes)



@app.route('/upload', methods=['POST'])
def upload():
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
    return render_template("emails.html")




if __name__ == '__main__':
    app.run(debug=True)
