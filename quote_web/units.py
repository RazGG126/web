from quote_web import mail

from flask_mail import Message
from flask import url_for


def send_reset_email(user):
    token = user.generate_token()
    msg = Message('Запрос на смену пароля', sender='noreply@quodis.com', recipients=[user.email])
    msg.body = f"""
    Чтобы сбросить ваш пароль, перейдите по данной ссылке (срок действия - 5 минут):
    {url_for('update_password', token=token, _external=True)}
    
    Если вы не делали данный запрос, проигнорируйте это письмо!
    Никаких изменений произведено не будет.
    
    Отвечать на данное письмо не нужно, так как оно сгенерировано автоматически.
    """

    mail.send(msg)



