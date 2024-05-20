from flask import redirect, url_for, session,request
import sqlite3
def calendarEvent_route(app) : 
    @app.route('/calendarEvent' ,methods=['POST'])
    def calendarEvent() : 
        if "email" not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
                eventTitle = request.form['eventTitle']
                eventDate = request.form.get('eventDate')
                eventDescription = request.form['eventDescription']
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                entries = (eventDate,eventTitle,eventDescription)
                c.execute("INSERT INTO Calendar (date_, title, description) VALUES (?, ?, ?)", entries)
                conn.commit()
                conn.close()

                return redirect(url_for("calendars"))