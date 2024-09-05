from flask import render_template, Flask, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash


from models import app, get_user_by_email, create_user, User


"""login_manager = LoginManager()
login_manager.init_app(app)"""


@app.route('/')
def index():
    """
    Возвращает домашнюю страницу
    :return: html
    """
    return render_template('index.html')


@app.route('/contacts')
def contacts():
    """
    Возвращает страницу с обратной связью
    :return: html
    """
    return render_template('contacts.html')


@app.route('/restaurants')
def restaurants():
    """
    Возвращает страницу с меню ресторанов
    :return: html
    """
    return render_template('restaurants.html')


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    """
    Возвращает страницу входа в аккаунт
    :return: html
    """
    if request.method == 'POST':
        info = list(dict(request.form).values())
        print(info)
        email, password = info[0], info[1]
        if not email or not password:
            flash('Все поля должны быть заполнены.')
            return redirect(url_for('log_in'))

        user = get_user_by_email(email)

        if not user:
            flash('Пользователя с такой почтой не существует.')
            return redirect(url_for('log_in'))

        if not check_password_hash(user.password_hash, password):
            flash('Пароль введен неправильно.', 'error')
            return redirect(url_for('log_in'))

        login_user(user)
        return redirect(url_for('user', email=email))

    return render_template('log_in.html')


@app.route('/sigh_up', methods=['GET', 'POST'])
def sigh_up():
    """
    Возвращает страницу регистрации
    :return: html
    """
    if request.method == 'POST':
        info = list(dict(request.form).values())
        name, email, password, repeat_password = info[0], info[1], info[2], info[3]
        if not (name and email and password and repeat_password):
            flash('Все поля должны быть заполнены.')
            return redirect(url_for('sigh_up'))

        if password != repeat_password:
            flash('Пароли не совпадают.')
            return redirect(url_for('sigh_up'))

        if get_user_by_email(email):
            flash('Пользователь с такой почтой уже существует.')
            return redirect(url_for('sigh_up'))

        create_user(1, name, email, password)

        flash("Вы успешно зарегистрированы! Пожалуйста, войдите в аккаунт.")
        return redirect(url_for('log_in'))

    return render_template('sigh_up.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
