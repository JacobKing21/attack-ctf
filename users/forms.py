from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, ValidationError, Length, EqualTo, InputRequired, DataRequired
from wtforms.widgets import TextArea

from app import users


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(max=12)])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField()


def login_check(form, field):
    user = users.query.filter_by(email=form.email.data).first()
    if user is None:
        raise ValidationError('User does not exist')
    elif not check_password_hash(user.password, form.password.data):
        raise ValidationError('Incorrect Password')


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[login_check])
    submit = SubmitField()


class SearchForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()


class BlogForm(FlaskForm):
    content = StringField(validators=[DataRequired()], widget=TextArea())
    submit = SubmitField()
    delete_submit = SubmitField('Delete all Blog Posts')
