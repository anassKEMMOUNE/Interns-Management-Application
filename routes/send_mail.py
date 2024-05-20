from email.message import EmailMessage
import smtplib
import traceback
import schedule
import time

def send_email():
    sender = "innovx_dch@outlook.com"
    recipients = ["anass.kemmoune@um6p.ma", "basma.arnaoui"]  # Add more recipients as needed
    subject = "Test Email"
    message = "Hello world!"
    password = "anassbasma123@"  # Use environment variables or a safer method to handle passwords

    email = EmailMessage()
    email["From"] = sender
    email["To"] = ", ".join(recipients)
    email["Subject"] = subject
    email.set_content(message)

    try:
        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587, timeout=100)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, recipients, email.as_string())
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        smtp.quit()

def send_mail():

    # Schedule the email to be sent every Monday at 9 AM
    schedule.every().monday.at("03:14").do(send_email)

