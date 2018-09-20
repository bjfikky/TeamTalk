import datetime

from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from peewee import *

DATABASE = MySQLDatabase('teamtalk', user='root', password='root', host='127.0.0.1', port=8889)


class Users(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists")
