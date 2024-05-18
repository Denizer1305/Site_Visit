import json
import math
import time
from flask import Blueprint, render_template, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from authorize.useful.forms import LoginForm, RegisterForm

user = Blueprint('authorize', __name__, template_folder='templates', static_folder='static')

db = None


@user.before_request
def before_request():
    # Подключение к базе
    global db
    db = g.get("link_db")


@user.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@user.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        if db:
            try:
                cur = db.cursor()
                cur.execute(f"SELECT count() as count FROM users WHERE name LIKE '{form.name.data}'")
                res = cur.fetchone()
                if res['count'] > 0:
                    flash("Такой пользователь уже есть", category="error")
                    print("Такой пользователь уже есть")
                    return redirect(url_for('authorize.register'))
                tm = math.floor(time.time())
                arr = []
                cur.execute("INSERT INTO users VALUES(NULL,?,?,?)", (form.name.data, hash, tm))
                cur.execute("INSERT INTO profiles VALUES(NULL,?,NULL,NULL,NULL,?,"
                            "NULL,NULL,NULL,?,0)", (form.name.data, form.email.data, json.dumps(arr)))
                db.commit()
                if res:
                    flash("Вы успешно зарегистрированы", category="success")
                    return redirect(url_for('authorize.login'))
                else:
                    flash("Ошибка при добавлении в БД", category="error")
            except sqlite3.Error as e:
                flash("Ошибка при добавлении в БД", category="error")
                print("Ошибка добавления в БД" + str(e))

    return render_template("authorize/register.html", title="Регистрация", form=form)


@user.route("/", methods=["POST", "GET"])
@user.route("/login", methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('adminPanel.index'))
    user_db = None
    form = LoginForm()
    if form.validate_on_submit():
        if db:
            try:
                cur = db.cursor()
                cur.execute(f'SELECT * FROM users WHERE name = "{form.name.data}" LIMIT 1')
                user_db = cur.fetchall()
                if not user_db:
                    print("Пользователь не найден. (authorize/login.py def login)")
                    flash("Пользователь не найден", "error")
                    return redirect(url_for('.login'))
            except sqlite3.Error as e:
                print(f'Ошибка авторизации. (authorize/login.py def login) {e}')
        if user_db and user_db[0]['name'] == form.name.data and check_password_hash(user_db[0]['psw'], form.psw.data):
            session['id'] = user_db[0]['id']
            session['name'] = user_db[0]['name']
            session['psw'] = user_db[0]['psw']
            print(f"Пользователь {session['name']} вошёл в аккаунт (authorize/login.py def login).")
            return redirect(url_for('adminPanel.index'))
        flash("Неверные данные  - логин", "error")

    return render_template("authorize/login.html", title="Войти", form=form)


@user.route("isLogged")
def isLogged():
    return True if session.get('name') else False


@user.route("logout")
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    name = session.pop('name', None)
    session.clear()
    print(f"Пользователь {name} вышел из аккаунта (authorize/login.py def logout). ")
    return redirect(url_for('.login'))
