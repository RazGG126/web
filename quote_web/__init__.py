from flask import Flask
from flask_ngrok import run_with_ngrok
from flask_login import LoginManager

from quote_web.data import db_session

app = Flask(__name__)

run_with_ngrok(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'x@uhg98(FUj9g8f9bz.s'

db_session.global_init("quote_web/db/quotes.db")

from quote_web import routes