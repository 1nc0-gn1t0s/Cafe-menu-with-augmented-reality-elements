from app_and_db import app, db


class Dish(db.Model):
    """
    Класс блюд
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    restaurant_chain = db.Column(db.Integer, nullable=False)
    features = db.Column(db.String(300), nullable=True)
    photo_path = db.Column(db.String(300), nullable=False)
    ar_path = db.Column(db.String(300), nullable=False)
    calories = db.Column(db.String(300), nullable=False)
    protein = db.Column(db.String(300), nullable=False)
    fats = db.Column(db.String(300), nullable=False)
    carbohydrates = db.Column(db.String(300), nullable=False)
    scale_x = db.Column(db.Integer, nullable=False)
    scale_y = db.Column(db.Integer, nullable=False)
    scale_z = db.Column(db.Integer, nullable=False)

    def __init__(self, title, restaurant_chain, photo_path,  ar_path, description, calories, protein, fats,
                 carbohydrates, features, scale_x, scale_y, scale_z):
        self.title = title
        self.restaurant_chain = restaurant_chain
        self.photo_path = photo_path
        self.ar_path = ar_path
        self.description = description
        self.calories = calories
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.protein = protein
        self.features = features
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z

    def __repr__(self):
        return '<Dish {}>'.format(self.title)


def delete_dish_by_id(dish_id):
    """
    Функция для удаления блюда по айди
    :param dish_id: dish_id
    :return: None
    """
    with app.app_context():
        dish = Dish.query.filter_by(id=dish_id).first()
        db.session.delete(dish)
        db.session.commit()


def get_dish_by_id(dish_id):
    """
    Функция для получения блюда по айди
    :param dish_id: dish_id
    :return: list
    """
    return Dish.query.filter_by(id=dish_id).first()


def get_chain_menu(chain_id):
    """
        Функция для получения меню определенного ресторана
        :param chain_id: chain_id
        :return: list
        """
    return Dish.query.filter_by(restaurant_chain=chain_id).all()


def create_dish(dish_name, description, chain, calories, protein, fats, carbohydrates, features, photo_path, ar_path,
                scale_x, scale_y, scale_z):
    """
    Функция для создания нового блюда
    :param dish_name: title
    :param description: description
    :param chain: restaurant_chain
    :param calories: calories
    :param protein: protein
    :param fats: fats
    :param carbohydrates: carbohydrates
    :param features: features
    :param photo_path: photo_path
    :param ar_path: ar_path
    :param scale_x: scale_x
    :param scale_y: scale_y
    :param scale_z: scale_z
    :return: Dish
    """
    new_dish = Dish(title=dish_name, description=description, features=features, restaurant_chain=chain,
                    calories=calories, protein=protein, fats=fats, carbohydrates=carbohydrates, photo_path=photo_path,
                    ar_path=ar_path, scale_x=scale_x, scale_y=scale_y, scale_z=scale_z)
    db.session.add(new_dish)
    db.session.commit()

    return new_dish