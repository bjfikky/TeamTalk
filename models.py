import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

from peewee import *

DATABASE = MySQLDatabase('teamtalk', user='root', password='root', host='127.0.0.1', port=8889)


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    def get_posts(self):
        return Post.select().where(Post.user == self)

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


class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='posts')
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
