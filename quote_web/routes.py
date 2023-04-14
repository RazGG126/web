from flask import render_template, redirect

from quote_web.forms.user import RegisterForm
from quote_web.data.users import User

from quote_web import app, db_session


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
                                   message="Такая почта уже зарегистрирована", mess_aleft=True)
        if db_sess.query(User).filter(User.nick_name == form.nick_name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Имя пользователя уже используется", mess_aleft=True)
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