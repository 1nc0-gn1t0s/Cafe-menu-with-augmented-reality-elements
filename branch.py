from user import User
from app_and_db import app, db


class Restaurant(db.Model):
    """
    Класс ресторанов
    """
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(300), nullable=False)
    chain = db.Column(db.Integer, nullable=False)

    def __init__(self, admin, manager, address, phone_number, chain):
        self.manager = manager
        self.address = address
        self.phone_number = phone_number
        self.admin = admin
        self.chain = chain

    def __repr__(self):
        return '<Restaurant {}>'.format(self.title)


def delete_branch_by_id(branch_id):
    """
    Функция для удаления ресторана по айди
    :param branch_id: branch_id
    :return:
    """
    with app.app_context():
        branch = Restaurant.query.filter_by(id=branch_id).first()
        manager = User.query.filter_by(id=branch.manager).first()
        db.session.delete(branch)
        db.session.delete(manager)
        db.session.commit()


def get_branch_by_id(branch_id):
    """
    Функция для получения блюда по айди
    :param branch_id: branch_id
    :return: Restaurant
    """
    return Restaurant.query.filter_by(id=branch_id).first()


def create_branch(manager, address, admin, phone_number, chain_id):
    """
    Функция для создания нового филиала
    :param manager: manager_id
    :param address: address
    :param admin: admin_id
    :param chain_id: chain_id
    :param phone_number: phone_number
    :return:
    """
    new_branch = Restaurant(admin=admin, manager=manager, address=address, chain=chain_id, phone_number=phone_number)
    db.session.add(new_branch)
    db.session.commit()


def get_branches_by_chain(chain_id):
    """
    Функция для получения филиалов конкретной ресторанной сети
    :param chain_id:
    :return: list
    """
    return Restaurant.query.filter_by(chain=chain_id).all()