import random
import os

from re import search
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, current_user

from app_and_db import app, db
from chain import get_chain_by_id, get_all_restaurants, get_admin_restaurants, create_chain
from dish import delete_dish_by_id, get_dish_by_id, get_chain_menu, create_dish
from other import get_all_cuisines, get_all_features, get_all_dish_features, send_email, send_notification, \
    delete_notification_by_id, get_all_notifications, Feature, Cuisine, DishFeature
from branch import delete_branch_by_id, get_branch_by_id, create_branch, get_branches_by_chain
from user import create_user, get_user_by_email, change_password, change_all_user_data, change_photo_and_ar_paths, \
    User, check_password_hash


login_manager = LoginManager()
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """
    Функция для поиска пользователя по id
    :param user_id: id
    :return: User
    """
    return User.query.get(int(user_id))


@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=str(e).split()[0])


@app.route('/')
def index():
    """
    Возвращает домашнюю страницу
    :return: html
    """
    return render_template('index.html')


@app.route('/contacts/success')
def success():
    """
    Возвращает страницу успешной отправки письма
    :return: html
    """
    return render_template('success.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    """
    Возвращает страницу с обратной связью
    :return: html
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        text = request.form.get('text')
        print(name)

        if not (name and email and text):
            flash('Все поля должны быть заполнены.')
            return redirect(url_for('contacts'))

        if '@' not in email:
            flash('Почта должна содержать знак "@".')
            return redirect(url_for('contacts'))

        mail = f'{name} отправил(а) письмо: \n{text} \nОтветьте на почту: {email}.'

        send_email('katapaskova947@gmail.com', mail)

        return redirect(url_for('success'))

    return render_template('contacts.html')


@app.route('/restaurants')
def restaurants():
    """
    Возвращает страницу с меню ресторанов
    :return: html
    """
    restaurant_chains = get_all_restaurants()

    return render_template('restaurants.html', restaurant_chains=restaurant_chains, features=get_all_features(),
                           cuisines=get_all_cuisines())


@app.route('/admin')
@login_required
def admin():
    """
    Возвращает страницу пользователя
    :return: html
    """
    user = current_user
    restaurant_chains = get_admin_restaurants(user.id)
    return render_template('admin.html', user=user, restaurant_chains=restaurant_chains)


@app.route('/admin/menu')
@login_required
def menu():
    """
    Возвращает страницу редактирования меню
    :return: html
    """
    user = current_user
    chain_id = session.get('chain_id')
    chain_menu = get_chain_menu(chain_id)
    chain = get_chain_by_id(chain_id)
    if chain.admin == user.id:
        return render_template('menu.html', user=user, menu=chain_menu, chain=chain)
    else:
        return redirect(url_for('admin'))


@app.route('/admin/branches')
@login_required
def branches():
    """
    Возвращает страницу с филиалами
    :return: html
    """
    user = current_user
    chain_id = session.get('chain_id')

    chain = get_chain_by_id(chain_id)
    chain_branches = get_branches_by_chain(chain_id)

    return render_template('branches.html', user=user, chain=chain, branches=chain_branches)


@app.route('/admin/branches/delete/<branch_id>')
@login_required
def delete_branch(branch_id):
    """
    Удаляет филиал
    :return: html
    """
    delete_branch_by_id(branch_id)

    return redirect(url_for('branches'))


@app.route('/admin/menu/delete/<dish_id>')
@login_required
def delete_dish(dish_id):
    """
    Удаляет блюдо
    :return: html
    """
    delete_dish_by_id(dish_id)

    return redirect(url_for('menu'))


@app.route('/manager/delete/<notification_id>')
@login_required
def delete_notification(notification_id):
    """
    Удаляет уведомление
    :return: html
    """
    delete_notification_by_id(notification_id)

    return redirect(url_for('manager'))


@app.route('/set_session/<chain_id>')
@login_required
def set_session(chain_id):
    """
    Функция для сохранения айди сети
    :return: None
    """
    session['chain_id'] = chain_id
    next_page = request.args.get('next')

    if next_page == 'branches':
        return redirect(url_for('branches'))
    elif next_page == 'menu':
        return redirect(url_for('menu'))


@app.route('/manager')
@login_required
def manager():
    """
    Возвращает страницу пользователя
    :return: html
    """
    user = current_user
    notifications = get_all_notifications(user.id)
    return render_template('manager.html', user=user, notifications=notifications)


@app.route('/log_in/<role>', methods=['GET', 'POST'])
def log_in(role):
    """
    Возвращает страницу входа в аккаунт
    :return: html
    """
    if request.method == 'POST':
        info = list(dict(request.form).values())
        email, password = info[0], info[1]
        if not email or not password:
            flash('Все поля должны быть заполнены.')
            return redirect(url_for('log_in', role=role))

        curr_user = get_user_by_email(email, role)

        if not curr_user:
            flash('Пользователя с такой почтой и ролью не существует.')
            return redirect(url_for('log_in', role=role))

        if not check_password_hash(curr_user.password_hash, password):
            flash('Пароль введен неправильно.', 'error')
            return redirect(url_for('log_in', role=role))

        login_user(curr_user)

        if curr_user.role == "admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('manager'))

    return render_template('log_in.html', role=role)


@app.route('/log_in/<role>/remind_password', methods=['GET', 'POST'])
def remind_password(role):
    """
    Возвращает страницу входа в аккаунт через код по почте
    :return: html
    """
    if request.method == 'POST':
        email = request.form.get('email')

        user = get_user_by_email(email, role)

        if not email:
            flash('Пожалуйста, введите почту.')
            return redirect(url_for('remind_password', role=role))

        if not user:
            flash('Пользователя с такой почтой не существует.')
            return redirect(url_for('remind_password', role=role))

        session['email'] = email
        return redirect(url_for('get_code', role=role))

    return render_template('remind_password.html')


@app.route('/log_in/<role>/remind_password/get_code', methods=['GET', 'POST'])
def get_code(role):
    """
    Возвращает страницу нажатия кнопки для получения кода
    :return: html
    """
    email = session.get('email')

    if request.method == 'POST':
        code = random.randint(1000, 10000)
        text = f'Ваш код для входа: {code}. Никому его не сообщайте.'
        send_email(email, text)
        session['code'] = code
        return redirect(url_for('new_password', role=role))

    return render_template('get_code.html', email=email)


@app.route('/log_in/<role>/remind_password/new_password', methods=['GET', 'POST'])
def new_password(role):
    """
    Возвращает страницу ввода кода из почты и создания нового пароля
    :return: html
    """
    email = session.get('email')

    if request.method == 'POST':
        code_sent = session.get('code')
        code = request.form.get('code')
        password = request.form.get('password')
        repeat_password = request.form.get('repeating')
        print(password, repeat_password)

        if str(code_sent).strip() != str(code).strip():
            flash('Введен неверный код.')
            return redirect(url_for('new_password'))

        if ' ' in password:
            flash('Пароль должен не содержать пробела.')
            return redirect(url_for('new_password'))

        if len(password) < 8:
            flash('Пароль должен состоять хотя бы из восьми знаков.')
            return redirect(url_for('new_password'))

        if not bool(search('[a-zA-Z]', password)):
            flash('Пароль должен содержать хотя бы одну строчную и одну заглавную буквы на латинице.')
            return redirect(url_for('new_password'))

        if password.lower() == password:
            flash('Пароль должен содержать хотя бы одну заглавную букву на латинице.')
            return redirect(url_for('new_password'))

        if password.upper() == password:
            flash('Пароль должен содержать хотя бы одну строчную букву на латинице.')
            return redirect(url_for('new_password'))

        if not bool(search(r'\d', password)):
            flash('Пароль должен содержать хотя бы одну цифру.')
            return redirect(url_for('new_password'))

        if password != repeat_password:
            flash('Пароли не совпадают.')
            return redirect(url_for('new_password'))

        change_password(email, password, role)

        return redirect(url_for('log_in', role=role))

    return render_template('new_password.html', email=email)


@app.route('/admin/new_chain', methods=['GET', 'POST'])
@login_required
def new_chain():
    """
    Возвращает первую страницу добавления новой сети ресторанов
    :return: html
    """
    user = current_user
    cuisines = get_all_cuisines()
    features = get_all_features()

    if request.method == 'POST':
        chain_name = request.form.get('chain_name')
        phone_number = request.form.get('phone_number')
        customer_cuisines = request.form.getlist('get_cuisines')
        customer_features = request.form.getlist('get_features')

        if not (chain_name and phone_number):
            flash('И название новой сети ресторанов, и номер телефона для связи должны быть введены.')
            return redirect(url_for('new_chain'))

        create_chain(chain_name, user.id, phone_number, ', '.join(customer_cuisines), ', '.join(customer_features))

        return redirect(url_for('admin'))

    return render_template('new_chain.html', user=user, cuisines=cuisines, features=features)


@app.route('/restaurants/restaurant_menu/<chain_id>', methods=['GET', 'POST'])  # фильтры
def restaurant_menu(chain_id):
    """
    Возвращает меню сети ресторанов
    :return: html
    """
    chain_menu = get_chain_menu(chain_id)
    return render_template('restaurant_menu.html', chain=get_chain_by_id(chain_id), menu=chain_menu)


@app.route('/admin/menu/new_dish', methods=['GET', 'POST'])
@login_required
def new_dish():
    """
    Возвращает первую страницу добавления нового блюда
    :return: html
    """
    user = current_user
    chain_id = session.get('chain_id')

    chain = get_chain_by_id(chain_id)
    dish_features = get_all_dish_features()
    cuisines = get_all_cuisines()

    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        description = request.form.get('description')
        calories = request.form.get('calories')
        protein = request.form.get('protein')
        fats = request.form.get('fats')
        carbohydrates = request.form.get('carbohydrates')
        get_dish_features = request.form.getlist('get_dish_features')
        photo_path = request.files.get('photo')
        ar_path = request.files.get('ar')
        scale_x = int(request.form.get('scale_x')) / 10
        scale_y = int(request.form.get('scale_y')) / 10
        scale_z = int(request.form.get('scale_z')) / 10

        if not (dish_name and calories and protein and fats and carbohydrates and photo_path and ar_path):
            flash('Все поля со звездочками должны быть заполнены.')
            return redirect(url_for('new_dish'))

        dish = create_dish(dish_name, description, chain.id, calories, protein, fats, carbohydrates,
                           ', '.join(get_dish_features), "", "", scale_x, scale_y, scale_z)

        print(f'static/dish_images/{chain.id}/{dish.id}.{photo_path.filename.rsplit(".", 1)[-1].lower()}',
              f'static/models/{chain.id}/{dish.id}.{ar_path.filename.rsplit(".", 1)[-1].lower()}')

        if not os.path.exists(f'static/dish_images/{chain.id}'):
            os.makedirs(f'static/dish_images/{chain.id}')
            photo_path.save(f'static/dish_images/{chain.id}/{dish.id}.{photo_path.filename.rsplit(".", 1)[-1].lower()}')
        else:
            photo_path.save(f'static/dish_images/{chain.id}/{dish.id}.{photo_path.filename.rsplit(".", 1)[-1].lower()}')

        if not os.path.exists(f'static/models/{chain.id}'):
            os.makedirs(f'static/models/{chain.id}')
            ar_path.save(f'static/models/{chain.id}/{dish.id}.{ar_path.filename.rsplit(".", 1)[-1].lower()}')
        else:
            ar_path.save(f'static/models/{chain.id}/{dish.id}.{ar_path.filename.rsplit(".", 1)[-1].lower()}')

        change_photo_and_ar_paths(dish.id,
                                  f'dish_images/{chain.id}/{dish.id}.{photo_path.filename.rsplit(".", 1)[-1].lower()}',
                                  f'models/{chain.id}/{dish.id}.{ar_path.filename.rsplit(".", 1)[-1].lower()}')

        return redirect(url_for('menu'))

    return render_template('new_dish.html', user=user, chain=chain, dish_features=dish_features, cuisines=cuisines)


@app.route('/admin/menu/new_branch', methods=['GET', 'POST'])
@login_required
def new_branch():
    """
    Возвращает первую страницу добавления нового филиала
    :return: html
    """
    curr_user = current_user
    chain_id = session.get('chain_id')

    chain = get_chain_by_id(chain_id)

    if request.method == 'POST':
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        repeating = request.form.get('repeating')

        if not (name and email and password and repeating and phone_number and address):
            flash('Все поля должны быть заполнены.')
            return redirect(url_for('new_branch'))

        user = get_user_by_email(email, 'manager')

        if user:
            flash('Менеджер с такой почтой уже существует.')
            return redirect(url_for('new_branch'))

        if '@' not in email:
            flash('Почта должна содержать знак "@".')
            return redirect(url_for('new_branch'))

        if ' ' in password:
            flash('Пароль должен не содержать пробела.')
            return redirect(url_for('new_branch'))

        if len(password) < 8:
            flash('Пароль должен состоять хотя бы из восьми знаков.')
            return redirect(url_for('new_branch'))

        if not bool(search('[a-zA-Z]', password)):
            flash('Пароль должен содержать хотя бы одну строчную и одну заглавную буквы на латинице.')
            return redirect(url_for('new_branch'))

        if password.lower() == password:
            flash('Пароль должен содержать хотя бы одну заглавную букву на латинице.')
            return redirect(url_for('new_branch'))

        if password.upper() == password:
            flash('Пароль должен содержать хотя бы одну строчную букву на латинице.')
            return redirect(url_for('new_branch'))

        if not bool(search(r'\d', password)):
            flash('Пароль должен содержать хотя бы одну цифру.')
            return redirect(url_for('new_branch'))

        if password != repeating:
            flash('Пароли не совпадают.')
            return redirect(url_for('new_branch'))

        create_user(name, email, password, role='manager')
        branch_manager = get_user_by_email(email, 'manager')
        create_branch(branch_manager.id, address, curr_user.id, phone_number, chain.id)
        link = 'https://arcafe.projectswhynot.site/log_in/manager'
        text = f'Доброго времени суток! Поздравляем, Вы стали менеджером ресторанной сети {chain.title}. ' + \
               f'Войдите в аккаунт по Вашей почте и паролю {password}. Вы сможете изменить пароль в настройках. ' + \
               f'Ссылка для входа в аккаунт: {link}'

        print(chain.title, password, link, text)

        send_email(email, text)

        return redirect(url_for('branches'))

    return render_template('new_branch.html')


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

        user = get_user_by_email(email, 'admin')

        if user:
            flash('Администратор с такой почтой уже существует.')
            return redirect(url_for('sigh_up'))

        if '@' not in email:
            flash('Почта должна содержать знак "@".')
            return redirect(url_for('sigh_up'))

        if ' ' in password:
            flash('Пароль должен не содержать пробела.')
            return redirect(url_for('sigh_up'))

        if len(password) < 8:
            flash('Пароль должен состоять хотя бы из восьми знаков.')
            return redirect(url_for('sigh_up'))

        if not bool(search('[a-zA-Z]', password)):
            flash('Пароль должен содержать хотя бы одну строчную и одну заглавную буквы на латинице.')
            return redirect(url_for('sigh_up'))

        if password.lower() == password:
            flash('Пароль должен содержать хотя бы одну заглавную букву на латинице.')
            return redirect(url_for('sigh_up'))

        if password.upper() == password:
            flash('Пароль должен содержать хотя бы одну строчную букву на латинице.')
            return redirect(url_for('sigh_up'))

        if not bool(search(r'\d', password)):
            flash('Пароль должен содержать хотя бы одну цифру.')
            return redirect(url_for('sigh_up'))

        if password != repeat_password:
            flash('Пароли не совпадают.')
            return redirect(url_for('sigh_up'))

        session['info'] = [name, email, password]

        code = random.randint(1000, 10000)
        text = f'Ваш код: {code}. Никому его не сообщайте.'
        send_email(email, text)
        session['code'] = code

        return redirect(url_for('check_email'))

    return render_template('sigh_up.html')


@app.route('/sigh_up/check_email', methods=['GET', 'POST'])
def check_email():
    """
    Возвращает страницу подтверждения почты
    :return: html
    """
    code_sent = session.get('code')
    info = session.get('info')
    name, email, password = info[0], info[1], info[2]
    if request.method == 'POST':
        code = request.form.get('code')

        if str(code_sent).strip() != str(code).strip():
            flash('Введен неверный код.')
            return redirect(url_for('check_email'))

        create_user(name, email, password)

        return redirect(url_for('log_in', role='admin'))

    return render_template('check_email.html', email=email)


@app.route('/ar_menu/<branch_id>', methods=['GET', 'POST'])
def ar_menu(branch_id):
    """
    Возвращает страницу AR-меню ресторана
    :return: html
    """
    branch = get_branch_by_id(branch_id)
    chain_id = branch.chain
    chain = get_chain_by_id(chain_id)
    chain_menu = get_chain_menu(chain_id)
    curr_table = session.get('table')

    return render_template('ar_menu.html', chain=chain, branch=branch, menu=chain_menu, table=curr_table)


@app.route('/ar_menu/<branch_id>/<dish_id>/ar', methods=['GET', 'POST'])
def ar(branch_id, dish_id):
    """
    Возвращает страницу с блюдом в AR
    :return: html
    """
    dish = get_dish_by_id(dish_id)
    branch = get_branch_by_id(branch_id)
    chain = get_chain_by_id(branch.chain)

    return render_template('ar.html', dish=dish, branch=branch, chain=chain)


@app.route('/ar_menu/<branch_id>/table', methods=['GET', 'POST'])
def table(branch_id):
    """
    Возвращает страницу с блюдом в AR
    :return: html
    """
    branch = get_branch_by_id(branch_id)
    chain = get_chain_by_id(branch.chain)

    if request.method == 'POST':
        session['table'] = request.form.get('table')

        return redirect(url_for('ar_menu', branch_id=branch_id))

    return render_template('table.html', chain=chain, branch=branch)


@app.route('/log_in_role')
def log_in_role():
    """
    Возвращает страницу выбора роли перед входом в аккаунт
    :return: html
    """
    return render_template('log_in_role.html')


@app.route('/change_data', methods=['GET', 'POST'])
@login_required
def change_data():
    """
    Возвращает страницу редактирования аккаунта
    :return: html
    """
    user = current_user

    if request.method == 'POST':
        email = user.email if not request.form.get('email') else request.form.get('email')
        name = user.name if not request.form.get('name') else request.form.get('name')
        password_new = request.form.get('password_new')
        password_new_repeating = request.form.get('password_new_repeating')

        if '@' not in email:
            flash('Почта должна содержать знак "@".')
            return redirect(url_for('change_data'))

        if not all([password_new, password_new_repeating]) and any([password_new, password_new_repeating]):
            flash('Должны быть заполнены либо и поле "Новый пароль", и поле "Повторите новый пароль", либо ни одно '
                  'из них.')
            return redirect(url_for('change_data'))

        elif password_new and password_new_repeating:
            if ' ' in password_new:
                flash('Пароль должен не содержать пробела.')
                return redirect(url_for('change_data'))

            if len(password_new) < 8:
                flash('Пароль должен состоять хотя бы из восьми знаков.')
                return redirect(url_for('change_data'))

            if not bool(search('[a-zA-Z]', password_new)):
                flash('Пароль должен содержать хотя бы одну строчную и одну заглавную буквы на латинице.')
                return redirect(url_for('change_data'))

            if password_new.lower() == password_new:
                flash('Пароль должен содержать хотя бы одну заглавную букву на латинице.')
                return redirect(url_for('change_data'))

            if password_new.upper() == password_new:
                flash('Пароль должен содержать хотя бы одну строчную букву на латинице.')
                return redirect(url_for('change_data'))

            if not bool(search(r'\d', password_new)):
                flash('Пароль должен содержать хотя бы одну цифру.')
                return redirect(url_for('change_data'))

            if password_new != password_new_repeating:
                flash('Пароли не совпадают.')
                return redirect(url_for('change_data'))

            change_password(user.email, password_new, user.role)

        change_all_user_data(user.email, user.role, email, name)

        return redirect('admin')

    return render_template('change_data.html', user=user)


@app.route('/order/<branch_id>/<dish_id>')
def order(dish_id, branch_id):
    """
    Функция для добавления блюда в заказ
    :return: html
    """
    dish = get_dish_by_id(dish_id)
    if not session.get('order'):
        user_order = [get_dish_by_id(dish_id)]
        session['user_order'] = user_order
    else:
        session['user_order'].append(get_dish_by_id(dish))
    print(session.get('user_order'))

    return redirect(url_for('ar_menu', branch_id=branch_id))


@app.route('/call_the_waiter/<branch_id>')
def call_the_waiter(branch_id):
    """
    Функция для вызова официанта
    :param branch_id: branch_id
    :return: html
    """
    curr_table = session.get('table')
    text = f'Вызов официанта. Столик {curr_table}.'
    branch = get_branch_by_id(branch_id)
    chain_id = branch.chain
    chain = get_chain_by_id(chain_id)
    send_notification(get_branch_by_id(branch_id).manager, text)

    return redirect(url_for('call_the_waiter_success', branch_id=branch_id, curr_table=curr_table, chain=chain))


@app.route('/call_the_waiter/<branch_id>/success')
def call_the_waiter_success(branch_id):
    """
    Страница успешной отправки сообщения менеджеру
    :param branch_id: branch_id
    :return: html
    """
    curr_table = session.get('table')
    branch = get_branch_by_id(branch_id)
    chain_id = branch.chain
    chain = get_chain_by_id(chain_id)
    curr_table = session.get('table')
    return render_template('call_the_waiter_success.html', branch=branch, curr_table=curr_table, chain=chain,
                           table=curr_table)


def get_titles_from_ids(id_string, model):
    if not id_string:
        return []

    ids = [int(x.strip()) for x in id_string.split(', ')]
    titles = db.session.query(model.title).filter(model.id.in_(ids)).all()
    return [title[0] for title in titles]


@app.template_filter('get_features')
def get_features(id_string):
    return get_titles_from_ids(id_string, Feature)


@app.template_filter('get_cuisines')
def get_cuisines(id_string):
    return get_titles_from_ids(id_string, Cuisine)


@app.template_filter('get_dish_features')
def get_dish_features(id_string):
    return get_titles_from_ids(id_string, DishFeature)


@app.route('/instruction')
def instruction():
    """
    Страница правил пользования
    :return: html
    """
    return render_template('instruction.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
