from flask import Flask
from flask import render_template
from data import db_session
from data.users import User
from data.quotes import Quote
from data.comments import Comment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'x@uhg98(FUj9g8f9bz.s'


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/sign-in')
def sign_in():
    return render_template('sign_in.html', title='Вход')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


if __name__ == '__main__':
    db_session.global_init("db/quotes.db")

    db_sess = db_session.create_session()

    quote = db_sess.query(Quote).filter(Quote.id == 2).first()
    for comment in quote.comments:
        print(comment)
    db_sess.commit()

    # app.run(port=8080, host='127.0.0.1')