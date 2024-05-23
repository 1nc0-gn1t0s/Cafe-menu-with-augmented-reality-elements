from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'just a really secret sentence'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    """
    Класс пользователя
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False)
    nickname = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    def __init__(self, nickname, username, password_hash):
        self.nickname = nickname
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return '<User {}>'.format(self.username)


def create_user(nickname, username, password):
    """
    Функция для добавления пользователя в базу данных
    :param nickname: nickname
    :param username: username
    :param password: password
    :return: None
    """
    new_user = User(nickname=nickname, username=username, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()


def get_user_by_username(username):
    """
    Функция для получения пользователя по username
    :param username: username
    :return: None
    """
    return User.query.filter_by(username=username).first()
