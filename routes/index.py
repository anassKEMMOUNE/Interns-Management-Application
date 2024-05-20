from flask import Flask, render_template, request, redirect, url_for, session,Response,send_from_directory
from Models.user import User
def index_route(app) : 
    @app.route('/')
    def index():
        if "email" not in session :
            return redirect(url_for('login'))
        

        try:
            user_data = User.get_all_users(exclude_admin=True)
            user_data =  user_data[:5]
            return render_template("index.html", users=user_data)
        
        except Exception as e:
            return f"An error occurred: {str(e)}"