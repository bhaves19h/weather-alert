from flask_mail import Mail
from flask_mail import Message

mail = Mail()

def send_alert_email(
    app,
    email,
    city,
    subject,
    body
):

    with app.app_context():

        msg = Message(
            subject=subject,
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        msg.body = body

        mail.send(msg)