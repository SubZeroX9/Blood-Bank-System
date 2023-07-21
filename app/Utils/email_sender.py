import smtplib
from email.message import EmailMessage
from dotenv import dotenv_values
from Utils.resource_finder import resource_path


def send_email(email, subject, body):
    config = dotenv_values(resource_path(".env"))
    user = config['MY_EMAIL']
    password = config['MY_EMAIL_PASSWORD']

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = email
    msg.set_content(body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    try:
        server.send_message(msg)
    except Exception as e:
        print("Could not send email, address is Invalid\n", e)
    server.quit()

def send_coupon_by_mail(email):
    subject = "Coupon Code"
    body = "Thanks for donating so many times! \n"
    body += "Here is your coupon code: " + "LATIMESUS25" + "\n"
    body += "You can use this coupon code to get a $25 discount on your next eligible order in AliExpress.\n"
    send_email(email, subject, body)
