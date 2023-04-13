from flask import Flask
from flask import render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm
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


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", mess_aleft=True)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", mess_aleft=True)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            nick_name=form.nick_name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/sign-in')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


if __name__ == '__main__':
    db_session.global_init("db/quotes.db")
    app.run(port=8080, host='127.0.0.1')