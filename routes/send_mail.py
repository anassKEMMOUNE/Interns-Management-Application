from flask import redirect, url_for,request
def send_email():
    from email.message import EmailMessage
    import smtplib
    import traceback

    sender = "innovx_dch@outlook.com"
    recipient = "anass.kemmoune@um6p.ma"
    message = "Hello world!"

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Test Email"
    email.set_content(message)

    try:
        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587, timeout=100)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, "anassbasma123@")
        smtp.sendmail(sender, recipient, email.as_string())
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        smtp.quit()


def send_email_route(app) :
    @app.route('/send_mail')
    def send_mail():
        send_email()
        return redirect(url_for("index"))