from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from app_and_db import db, app

import smtplib


class DishFeature(db.Model):
    """
    Класс описаний блюд
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<DishFeature {}>'.format(self.title)


class Cuisine(db.Model):
    """
    Класс кухонь мира
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Cuisine {}>'.format(self.title)


class Feature(db.Model):
    """
    Класс кухонь мира
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Feature {}>'.format(self.title)


class Notification(db.Model):
    """
    Класс уведомлений менеджера
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    manager = db.Column(db.Integer, nullable=False)

    def __init__(self, text, manager):
        self.text = text
        self.manager = manager

    def __repr__(self):
        return '<Notification {}>'.format(self.text)


def send_notification(manager_id, text):
    """
    Функция для отправки уведомления менеджеру ресторана
    :param manager_id: manager_id
    :param text: text
    :return: None
    """
    new_notification = Notification(text=text, manager=manager_id)
    db.session.add(new_notification)
    db.session.commit()


def get_all_dish_features():
    """
    Функция для получения всех описаний блюд
    :return: list
    """
    return DishFeature.query.all()


def get_all_cuisines():
    """
    Функция для получения всех кухонь мира из базы данных
    :return: list
    """
    return Cuisine.query.all()


def get_all_features():
    """
    Функция для получения всех ресторанных фишек из базы данных
    :return: list
    """
    return Feature.query.all()


def send_email(email, text):
    """
    Функция для отправки сообщения на почту
    :param email: email
    :param text: text
    :return: None
    """
    msg = MIMEMultipart()
    msg['From'] = 'katapaskova947@gmail.com'
    msg['To'] = email
    msg['Subject'] = Header('Важное сообщение от CafeAR!', 'utf-8')

    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('katapaskova947@gmail.com', 'uaao pdzg fepr idex')

    try:
        smtp_server.sendmail('katapaskova947@gmail.com', email, msg.as_string())
    except smtplib.SMTPException as e:
        print(f'Ошибка при отправке письма: {e}')
    finally:
        smtp_server.quit()


def delete_notification_by_id(notification_id):
    """
    Функция для удаления уведомления по айди
    :param notification_id: notification_id
    :return: None
    """
    with app.app_context():
        notification = Notification.query.filter_by(id=notification_id).first()
        db.session.delete(notification)
        db.session.commit()


def get_all_notifications(manager_id):
    """
    Функция для получения всех уведомлений
    :param manager_id: manager_id
    :return: list
    """
    return Notification.query.filter_by(manager=manager_id).all()
