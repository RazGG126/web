from flask import Flask
from flask_ngrok import run_with_ngrok
from flask_login import LoginManager
from flask_mail import Mail
from quote_web.data import db_session

app = Flask(__name__)

run_with_ngrok(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'x@uhg98(FUj9g8f9bz.s'

db_session.global_init("quote_web/db/quotes.db")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'discussquote@gmail.com'
app.config['MAIL_PASSWORD'] = 'qjqccoguxyqystaa'

mail = Mail(app)

from quote_web import routes