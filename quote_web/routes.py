from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from quote_web.forms.user import RegisterForm, LoginForm
from quote_web.forms.quote import QuoteForm
from quote_web.data.users import User
from quote_web.data.quotes import Quote

from quote_web import app, db_session, login_manager


@app.route('/')
def index():
    db_sess = db_session.create_session()
    quotes = db_sess.query(Quote).all()
    no_quotes = False
    if len(quotes) == 0:
        no_quotes = True
    return render_template('home.html', title='Главная', quotes=quotes, no_quotes=no_quotes)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/quote',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = QuoteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        quote = Quote()
        quote.author = form.author.data
        quote.content = form.content.data
        current_user.quotes.append(quote)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('quote.html', title='Добавление цитаты',
                           form=form)


@app.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    return redirect("/sign-in")


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form, mess_aleft=True)
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", mess_aleft=True)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nick_name == form.nick_name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Имя пользователя уже используется", mess_aleft=True)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такая почта уже зарегистрирована", mess_aleft=True)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            nick_name=form.nick_name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')