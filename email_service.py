import smtplib, ssl
import os
from email.message import EmailMessage


port = 465
smtp_server = "smtp.gmail.com"
sender_email = 'aakash21696@gmail.com'
password = os.environ['EMAIL_PASS']


def send_email(message, tolist):
    print("Sending email with message: {}".format(message))
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Vaccine Update'
    msg['From'] = "Aakash Mishra"
    msg['To'] = tolist

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()