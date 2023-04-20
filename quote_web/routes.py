from flask import render_template, redirect, request, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from quote_web.forms.user import RegisterForm, LoginForm, ResetPasswordForm, UpdatePasswordForm
from quote_web.forms.quote import QuoteForm
from quote_web.forms.comment import CommentForm

from quote_web.units import send_reset_email


from quote_web.data.users import User
from quote_web.data.quotes import Quote
from quote_web.data.comments import Comment
from quote_web.data.likes import Like

from quote_web.check_password import check_password

from quote_web import app, db_session, login_manager


@app.route('/')
def index():
    db_sess = db_session.create_session()
    quotes = db_sess.query(Quote).order_by(Quote.created_date.desc()).all()
    no_quotes = False
    if len(quotes) == 0:
        no_quotes = True
    return render_template('home.html', title='Главная', quotes=quotes, no_quotes=no_quotes)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/quote-add', methods=['GET', 'POST'])
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
    return render_template('quote_add.html', title='Новая цитата',
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
                               form=form, mess_alert=True)
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", mess_alert=True)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nick_name == form.nick_name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Имя пользователя уже используется", mess_alert=True)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такая почта уже зарегистрирована", mess_alert=True)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            nick_name=form.nick_name.data
        )

        checked = check_password(form.password.data)

        if not checked[0]:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message=checked[1], mess_alert=True)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/quote/<int:id>', methods=['GET', 'POST'])
def quote(id):
    form = CommentForm()
    db_sess = db_session.create_session()
    quote = db_sess.query(Quote).filter(Quote.id == id).first()
    comments = db_sess.query(Comment).order_by(Comment.id.desc()).filter(Comment.quote_id == id).all()
    quote.comments_number = len(comments)
    db_sess.commit()
    if form.validate_on_submit():
        comment = Comment(
            content=form.comment.data,
            user_id=current_user.id,
            quote_id=id
        )
        db_sess.add(comment)
        db_sess.commit()
        return redirect(f'/quote/{id}')
    return render_template('quote.html',
                           title='Цитата',
                           quote=quote,
                           comments=comments,
                           form=form)


@app.route('/like-quote/<int:quote_id>', methods=['POST'])
@login_required
def like(quote_id):
    db_sess = db_session.create_session()
    quote = db_sess.query(Quote).filter(Quote.id == quote_id).first()
    like = db_sess.query(Like).filter(Like.user_id == current_user.id, Like.quote_id == quote_id).first()
    if not quote:
        jsonify({"error": 'Quote does not exist.'}, 400)
    elif like:
        db_sess.delete(like)
        quote.likes_number = quote.likes_number - 1
        db_sess.commit()
    else:
        like = Like(user_id=current_user.id, quote_id=quote_id)
        db_sess.add(like)
        quote.likes_number = quote.likes_number + 1
        db_sess.commit()
    return jsonify({"likes": quote.likes_number, "liked": current_user.id in map(lambda x: x.user_id, quote.likes)})


def send_mail():
    pass


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect('/')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('reset_password.html', title='Сброс пароля', form=form, mess_alert=True,
                                   message='Аккаунт с такой почтой не найден.')
        send_reset_email(user)
        return redirect('/sign-in')
    return render_template('reset_password.html', title='Сброс пароля', form=form)


@app.route('/update_password/<token>', methods=['GET', 'POST'])
def update_password(token):
    user_id = User.verify_token(token)

    if user_id is None:
        return 'error'

    form = UpdatePasswordForm()
    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", mess_alert=True)

        checked = check_password(form.password.data)

        if not checked[0]:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message=checked[1], mess_alert=True)

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()

        user.set_password(form.password.data)
        db_sess.commit()

        return redirect('/sign-in')

    return render_template('update_password.html', title='Сброс пароля', form=form)
