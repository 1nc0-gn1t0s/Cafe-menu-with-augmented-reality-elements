from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'there will be something here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    """
    Класс пользователя
    """
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, primary_key=False, nullable=False)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    def __init__(self, role, name, email, password_hash):
        self.role = role
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '<User {}>'.format(self.name)


class RestaurantChain(db.Model):
    """
    Класс сетей ресторанов
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    admin = db.Column(db.Integer, nullable=False)

    def __init__(self, title, admin):
        self.title = title
        self.admin = admin


class Restaurant(db.Model):
    """
    Класс ресторанов
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    manager = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    contacts = db.Column(db.String(300), nullable=False)

    def __init__(self, title, manager, address, contacts):
        self.title = title
        self.manager = manager
        self.address = address
        self.contacts = contacts

    def __repr__(self):
        return '<Restaurant {}>'.format(self.title)


class Dish(db.Model):
    """
    Класс блюд
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    restaurant_chain = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String(300), nullable=False)
    ar_path = db.Column(db.String(300), nullable=False)

    def __init__(self, title, restaurant_chain, photo_path,  ar_path):
        self.title = title
        self.restaurant_chain = restaurant_chain
        self.photo_path = photo_path
        self.ar_path = ar_path

    def __repr__(self):
        return '<Dish {}>'.format(self.title)


def create_user(role, name, email, password):
    """
    Функция для добавления пользователя в базу данных
    :param role: role
    :param name: name
    :param email: email
    :param password: password
    :return: None
    """
    new_user = User(role=role, name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()


def get_user_by_email(email):
    """
    Функция для получения пользователя по username
    :param email: email
    :return: None
    """
    return User.query.filter_by(email=email).first()


def check_password(user, password):
    """
    Функция для проверки пароля
    :param user: user
    :param password: password
    :return: Bool
    """
    return check_password_hash(user.password_hash, password)
