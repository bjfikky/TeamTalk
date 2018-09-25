from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User


def username_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that username already exists')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email address already exists')


class RegistrationForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$', message=("Username should be one word, letters "
                                                "numbers, and underscore only")
                   ),
            username_exists
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4),
            EqualTo('password2', message="Passwords must match")
        ]
    )

    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(Form):
    content = TextAreaField(
        'Update',
        validators=[
            DataRequired(),
            Length(min=5, message="Post must be a minimum of 5 characters"),
        ]
    )
