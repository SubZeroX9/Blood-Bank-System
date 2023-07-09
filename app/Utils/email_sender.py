import smtplib
from email.message import EmailMessage
from dotenv import dotenv_values


def send_email(email, subject, body):
    config = dotenv_values(".env")
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
    server.send_message(msg)
    server.quit()
