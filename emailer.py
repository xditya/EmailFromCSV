from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from texts import texts

sender_email = config("SENDER_EMAIL", default=None)
sender_password = config("SENDER_PASSWORD", default=None)

if not sender_email or not sender_password:
    raise Exception("Please provide sender email and password")

# with open("content.html") as f:
#     data = f.read()

data = "hello there <#name>"


def send_email(email_name_list):
    done = []
    failed = []
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        for name, email in email_name_list:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = texts.SUBJECT
            data = data.replace("<#name>", name)

            message.attach(MIMEText(data, "plain"))
            # message.attach(MIMEText(data, "html"))

            try:
                server.sendmail(sender_email, email, message.as_string())
                done.append(email)
            except Exception as e:
                failed.append(email)
                print(f"Error sending to {email}: {e}")
    return done, failed
