import sqlite3
import psycopg2
import os
from flask import Flask, flash, request, redirect, url_for, g, render_template

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Config import db_name
from database import Database
from Forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin

DATABASE = f'/tmp/{db_name}.db'
DEBUG = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
SECRET_KEY = 'fc67934b56faafe32815'
MAX_CONTENT_LENGTH = 1024 * 8

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, f'{db_name}.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

# создание таблицы потом нужно понять где вызывать
def CreateDb():
    db = Database()
    db.create_db()
    db.Close()


#Установление соединения с БД перед выполнением запроса
dbase = None
@app.before_request
def BeforeRequest():
    global dbase
    dbase = Database()

#Закрываем соединение с БД, если оно было установлено
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def start():
    return render_template('start.html')



@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().Create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            hash = generate_password_hash(request.form['password'])
            res = dbase.add_data_user(form.last_name.data, form.first_name.data, form.middle_name.data, form.email.data, form.login.data, hash)
            if res[0]:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                print(form.errors)
                flash("Ошибка при добавлении в БД: "+res[1], "error")

    return render_template("register.html", title="Регистрация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", title="Профиль")


if __name__ == "__main__":
    app.run(debug=True)
