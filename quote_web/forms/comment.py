from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from markupsafe import Markup
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment = StringField('Автор цитаты', validators=[DataRequired()])
    submit_value = Markup('<i class="fa-regular fa-paper-plane" style="color: #ffa50a;"></i>')
    submit = SubmitField(submit_value)