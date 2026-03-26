from threading import Thread

from flask import current_app
from flask_mail import Message

from project.extensions import mail


def _deliver_message(app, message) -> None:
    with app.app_context():
        mail.send(message)


def send_email(subject: str, recipients: list[str], html_body: str):
    app = current_app._get_current_object()
    message = Message(subject, recipients=recipients)
    message.html = html_body

    if not app.config.get('MAIL_SEND_ASYNC', True):
        _deliver_message(app, message)
        return None

    thread = Thread(
        target=_deliver_message,
        args=(app, message),
        daemon=True,
        name='mail-sender',
    )
    thread.start()
    return thread
