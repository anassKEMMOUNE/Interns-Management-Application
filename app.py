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
from routes.send_mail import send_mail


from flask import Flask
# from apscheduler.schedulers.background import BackgroundScheduler
from email.message import EmailMessage
import smtplib
import traceback


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



# def send_email(sender, recipients, subject, message, password):
#     email = EmailMessage()
#     email["From"] = sender
#     email["To"] = ", ".join(recipients)
#     email["Subject"] = subject
#     email.set_content(message)

#     try:
#         smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587, timeout=100)
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.login(sender, password)
#         smtp.sendmail(sender, recipients, email.as_string())
#     except Exception as e:
#         print("An error occurred:", e)
#         traceback.print_exc()
#     finally:
#         smtp.quit()

# def send_mail():
#     sender = "innovx_DCH@outlook.com"
#     recipients = ["anass.kemmoune@um6p.ma", "basma.arnaoui@um6p.ma"]  # Add more recipients as needed
#     subject = "Test Email"
#     message = "Hello world!"
#     password = "anassbasma123@"  # Use environment variables or a safer method to handle passwords

#     send_email(sender, recipients, subject, message, password)

# def schedule_email():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(send_mail, 'cron', day_of_week='mon', hour=3, minute=23)
#     scheduler.start()

# schedule_email()  

if __name__ == '__main__':
    app.run(debug=True)
