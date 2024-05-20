from flask import render_template, redirect, url_for, session
from Models.user import User

def emails_route(app) : 
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
            return str(e)