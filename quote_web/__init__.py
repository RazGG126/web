from flask import Flask

from quote_web.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'x@uhg98(FUj9g8f9bz.s'
db_session.global_init("quote_web/db/quotes.db")

from quote_web import routes