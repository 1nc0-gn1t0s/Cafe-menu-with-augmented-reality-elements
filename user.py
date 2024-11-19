from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


from app_and_db import db
from dish import get_dish_by_id


class User(db.Model, UserMixin):
    """
    Класс пользователя
    """
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(300), primary_key=False, nullable=False)
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


def create_user(name, email, password, role="admin"):
    """
    Функция для добавления пользователя в базу данных
    :param role: role
    :param name: name
    :param email: email
    :param password: password
    :return: None
    """
    new_user = User(role=role, name=name, email=email,
                    password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()


def get_user_by_email(email, role):
    """
    Функция для получения пользователя по email
    :param role: role
    :param email: email
    :return: None
    """
    return User.query.filter_by(email=email, role=role).first()


def check_password(user, password):
    """
    Функция для проверки пароля
    :param user: user
    :param password: password
    :return: Bool
    """
    return check_password_hash(user.password_hash, password)


def change_password(email, password, role):
    """
    Функция для изменения пароля пользователя
    :param email: email
    :param password: new password
    :param role: role
    :return: None
    """
    user = get_user_by_email(email, role)
    user.password_hash = generate_password_hash(password)
    db.session.commit()


def change_all_user_data(user_email, user_role, email, name):
    """
    Функция для изменения данных пользователя
    :param user_email:
    :param user_role:
    :param email:
    :param name:
    :return:
    """
    user = get_user_by_email(user_email, user_role)
    user.email = email
    user.name = name
    db.session.commit()


def change_photo_and_ar_paths(dish_id, photo_path, ar_path):
    """
    Функция для изменения путя к фото и AR-модели блюда
    :param dish_id: dish_id
    :param photo_path: photo_path
    :param ar_path: AR_path
    :return: None
    """
    dish = get_dish_by_id(dish_id)
    dish.photo_path = photo_path
    dish.ar_path = ar_path
    db.session.commit()



