import sqlite3
import psycopg2
import os
from flask import Flask, flash, request, redirect, url_for, g, render_template

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Config import db_name, hanle_input, file_input
from database import Database
from Forms import RegisterForm, LoginForm, AddTaskForm, AddBankForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
from Parser import Parse
from TestClasses.Kit import Kit
from Interface import add_kit_content, delete_bank

DATABASE = f'/tmp/{db_name}.db'
DEBUG = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
SECRET_KEY = 'fc67934b56faafe32815'
MAX_CONTENT_LENGTH = 1024 * 8

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(dict(DATABASE=os.path.join(app.root_path, f'{db_name}.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

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
def closeDb(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
    


@app.route("/")
def start():
    if current_user.is_authenticated:
        return redirect(url_for('showBanks'))
    else:
        return render_template('main.html')

@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html")

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
    if form.validate_on_submit() and form.conf_flag:
            hash = generate_password_hash(request.form['password'])
            res = dbase.add_data_user(form.last_name.data, form.first_name.data, form.middle_name.data, form.email.data, form.login.data, hash)
            if res[0]:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                print(form.errors)
                flash(res[1], "error")

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


@app.route('/add_test', methods=["POST", "GET"])
@login_required
def addTest():
    form = AddTaskForm() 
    res = dbase.get_banks_by_id(current_user.get_id())
    if res:
        form.bank_id.choices = [(bank_id, bank_name) for bank_id, bank_name in res]
    if form.validate_on_submit():
        kit = Kit(form.name.data)
        if form.file.data:
            create_upload_folder()
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf8') as file:
                input = file.read()
            Parse(form.name.data, input, kit, form.test_mode.data, file_input)
        elif form.text.data:
            input = form.text.data
            Parse(form.name.data, input, kit, form.test_mode.data, hanle_input)
        else:
            flash("Введите текст или загрузите файл", "error")
            return(redirect(url_for('addTest')))
        
        
        if add_kit_content(dbase, kit, form.bank_id.data):
            flash("Тест добавлен", "success")
        else:
            flash("Произошла ошибка при добавлении теста", "error")
        return redirect(url_for('showBanks'))
    return render_template('add_test.html', title = "Добавление теста", form = form)

@app.route('/my_banks', methods=["POST", "GET"])
@login_required
def showBanks():
    banks = dbase.get_banks_by_id(current_user.get_id())
    return render_template('show_banks.html', banks = banks, dbase = dbase)

@app.route('/add_bank', methods=["POST", "GET"])
@login_required
def addBank():
    form = AddBankForm()
    if form.validate_on_submit():
        res = dbase.add_data_bank(current_user.get_id(), form.name.data)
        if res:
            flash("Набор создан", "success")
            return redirect(url_for('showBanks'))
        else:
            flash(res[1], "error")

    return render_template('add_bank.html', form = form)

@app.route('/show_test/<test_id>', methods=["POST", "GET"])
@login_required
def showTest(test_id):
    res = dbase.get_tasks_by_test_id(test_id)
    return render_template('show_tests.html', dbase = dbase, tasks = res)

if __name__ == "__main__":
    app.run(debug=True)
