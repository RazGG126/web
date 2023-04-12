from flask import Flask
from flask import render_template

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
    app.run(port=8080, host='127.0.0.1')