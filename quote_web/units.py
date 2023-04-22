import os
import shutil
import secrets

from quote_web import mail

from flask_mail import Message
from flask import url_for, current_app

from PIL import Image


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


def add_default_profile_image(user):
    full_path = os.path.join(os.getcwd(), 'quote_web\\static', 'profiles_pics', str(user.id))
    if not os.path.exists(full_path):
        os.mkdir(full_path)
        full_path += '\\profile_images'
        os.mkdir(full_path)
    shutil.copy(f'{os.getcwd()}\\quote_web\\static\\profiles_pics\\default.png', full_path)


def save_profile_image(form_picture, user):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'profiles_pics', str(user.id), 'profile_images')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    else:
        for f in os.listdir(full_path):
            os.remove(os.path.join(full_path, f))

    picture_path = os.path.join(full_path, picture_fn)
    img = Image.open(form_picture)
    img.resize((100, 100)).save(picture_path)

    return picture_fn

