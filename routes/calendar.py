from flask import render_template, redirect, url_for, session
from Models.user import User
import sqlite3
import os
import json

def calendars_route(app) :
    @app.route('/calendar')
    def calendars():
        if "email" not in session:
            return redirect(url_for('login'))

        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(os.path.abspath("") +'/database.db')
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
            with open(os.path.abspath("")+'/static/json/calendar_data.json', 'w') as json_file:
                json.dump(calendar_data, json_file)

            # Render the template
            return render_template("calendar.html")

        except Exception as e:
            return render_template("error.html", error=str(e))