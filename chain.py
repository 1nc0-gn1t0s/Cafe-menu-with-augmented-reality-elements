from app_and_db import db


class RestaurantChain(db.Model):
    """
    Класс сетей ресторанов
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    cuisines = db.Column(db.String(300), nullable=True)
    features = db.Column(db.String(300), nullable=True)

    def __init__(self, title, admin, phone_number, cuisines, features):
        self.title = title
        self.admin = admin
        self.phone_number = phone_number
        self.cuisines = cuisines
        self.features = features

    def __repr__(self):
        return '<RestaurantChain {}>'.format(self.title)


def get_admin_restaurants(admin_id):
    """
    Функция для получения всех сетей ресторанов, созданных определенным админом
    :param admin_id: admin_id
    :return: list
    """
    return RestaurantChain.query.filter_by(admin=admin_id).all()


def get_chain_by_id(chain_id):
    """
    Функция для получения сети ресторанов по айди
    :param chain_id: chain_id
    :return: RestaurantChain
    """
    return RestaurantChain.query.filter_by(id=chain_id).first()


def get_all_restaurants():
    """
    Функция для получения всех сетей ресторанов
    :return: list
    """
    return RestaurantChain.query.all()


def create_chain(title, admin, phone, cuisines, features):
    """
    Функция для добавления пользователя в базу данных
    :param title: title
    :param admin: admin
    :param phone: phone
    :param cuisines: cuisines
    :param features: features
    :return: None
    """
    new_chain = RestaurantChain(title=title, admin=admin, phone_number=phone, cuisines=cuisines, features=features)
    db.session.add(new_chain)
    db.session.commit()

