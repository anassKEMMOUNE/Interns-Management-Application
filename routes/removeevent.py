from flask import redirect, url_for,request,render_template,session
import sqlite3
from Models.user import User
import os



def removeevent_route(app) : 
    @app.route('/removeevent',methods = ['POST'])
    def removeevent():
        if "email" not in session:
            return redirect(url_for('login'))
        try :
            data = request.get_json()
            unique_id = data.get('unique_class')  
            unique_id = unique_id.replace("_"," ")
            print(unique_id)
            conn = User.connect_to_database(os.path.abspath("") +'/database.db')
            c = conn.cursor()
            c.execute("DELETE FROM Calendar WHERE title=?", (unique_id,))
            conn.commit()
            conn.close()

            return redirect(url_for("calendars"))
        except :
            return
