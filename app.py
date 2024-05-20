from flask import Flask,session
from routes.index import index_route
from routes.login import login_route
from routes.settings import settings_route
from routes.cvfilter import cvfilter_route
from routes.upload import upload_route
from routes.emails import emails_route
from routes.calendar import calendars_route
from routes.get_resume import get_resume_route
from routes.calendarEvent import calendarEvent_route
from routes.removeevent import removeevent_route
from routes.send_mail import send_email_route

app = Flask(__name__)
app.secret_key = 'innovx'



index_route(app)
login_route(app)
settings_route(app)
cvfilter_route(app)
upload_route(app)
emails_route(app)
calendars_route(app)
get_resume_route(app)
calendarEvent_route(app)
removeevent_route(app)
send_email_route(app)


if __name__ == '__main__':
    app.run(debug=True)
