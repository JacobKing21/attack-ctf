from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, ValidationError, Length, EqualTo, InputRequired, DataRequired
from wtforms.widgets import TextArea


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(max=12)])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField()


class SearchForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()


class BlogForm(FlaskForm):
    content = StringField(validators=[DataRequired()], widget=TextArea())
    submit = SubmitField()
    delete_submit = SubmitField('Delete all Blog Posts')
