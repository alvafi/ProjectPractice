import sqlite3
import psycopg2
import os
from flask import Flask, flash, request, redirect, url_for, g, render_template, send_file

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from Config import db_name, hanle_input, file_input
from database import Database
from Forms import RegisterForm, LoginForm, AddTaskForm, AddTaskToExistingKitForm, AddBankForm, ChangeName, ExportTestForm, ChangeAnswerForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
from Parser import Parse
from TestClasses.Kit import Kit
from Interface import add_kit_content, delete_bank, delete_kit, edit_bank_name, edit_kit_name, edit_test_name, delete_test, add_kit_content_to_existing_kit, delete_task, edit_task_question, edit_answer, delete_answer, add_answer
from Export import Export

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


@app.route('/add_test_to_kit/<kit_id>', methods=["POST", "GET"])
@login_required
def addTestToExistingKit(kit_id):
    form = AddTaskToExistingKitForm() 
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
            return(redirect(url_for('addTestToExistingKit', kit_id = kit_id)))
        
        
        if add_kit_content_to_existing_kit(dbase, kit, kit_id):
            flash("Тест добавлен", "success")
        else:
            flash("Произошла ошибка при добавлении теста", "error")
        return redirect(url_for('showBanks'))
    return render_template('add_test_to_existing_kit.html', title = "Добавление теста", form = form, kit_id = kit_id)

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

@app.route('/delete_bank/<bank_id>', methods=["POST", "GET"])
@login_required
def deleteBank(bank_id):
    if delete_bank(dbase, bank_id):
        flash("Набор удален", "success")
    else:
        flash("Ошибка при удалении набора", "error")
    return redirect (url_for('showBanks'))

@app.route('/delete_kit/<kit_id>', methods=["POST", "GET"])
@login_required
def deleteKit(kit_id):
    if delete_kit(dbase, kit_id):
        flash("Тесты удалены", "success")
    else:
        flash("Ошибка при удалении тестов", "error")
    return redirect (url_for('showBanks'))


@app.route('/change_bank_name/<bank_id>', methods=["POST", "GET"])
@login_required
def changeBankName(bank_id):
    form = ChangeName()
    if form.validate_on_submit():
        if edit_bank_name(dbase, bank_id, form.name.data):
            flash("Название успешно изменино", "success")
            return redirect(url_for('showBanks'))
        else:
            flash("Произошла ошибка при изменении названия", "error")
            return redirect(url_for('showBanks'))
    return render_template('change_name.html', bank_id = bank_id,  form = form)

@app.route('/change_kit_name/<kit_id>', methods=["POST", "GET"])
@login_required
def changeKitName(kit_id):
    form = ChangeName()
    if form.validate_on_submit():
        if edit_kit_name(dbase, kit_id, form.name.data):
            flash("Название успешно изменино", "success")
            return redirect(url_for('showBanks'))
        else:
            flash("Произошла ошибка при изменении названия", "error")
            return redirect(url_for('showBanks'))
    return render_template('change_name.html', kit_id = kit_id, form = form)

@app.route('/change_test_name/<test_id>', methods=["POST", "GET"])
@login_required
def changeTestName(test_id):
    form = ChangeName()
    if form.validate_on_submit():
        if edit_test_name(dbase, test_id, form.name.data):
            flash("Название успешно изменино", "success")
            return redirect(url_for('showBanks'))
        else:
            flash("Произошла ошибка при изменении названия", "error")
            return redirect(url_for('showBanks'))
    return render_template('change_name.html', test_id = test_id, form = form)


@app.route('/export_test/<test_id>', methods=["POST", "GET"])
@login_required
def exportTest(test_id):
    form = ExportTestForm()
    if form.validate_on_submit():
        data = Export(dbase, test_id, form.export_type.data)
        if data:
            test_name = dbase.get_test_name_by_test_id(test_id)
            print(test_name)
            if not test_name:
                test_name = "test"
            
            flash("Тест успешно экспортирован", "success")
            return send_file(data, as_attachment=True, download_name=str(test_name + '.' +  form.export_type.data))
            
        else:
            flash("Произошла ошибка при экспорте теста", "error")
            return redirect(url_for('showBanks'))
    return render_template("export_test.html", form = form)


@app.route('/show_test/<test_id>', methods=["POST", "GET"])
@login_required
def showTest(test_id):
    res = dbase.get_tasks_by_test_id(test_id)
    return render_template('show_tests.html', dbase = dbase, tasks = res, test_id = test_id)


@app.route('/delete_test/<test_id>', methods=["POST", "GET"])
@login_required
def deleteTest(test_id):
    if delete_test(dbase, test_id):
        flash("Тест удален", "success")
    else:
        flash("Ошибка при удалении теста", "error")
    return redirect (url_for('showBanks'))

@app.route('/edit_task/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def editTask(task_id, test_id):
    return render_template('show_task.html', dbase = dbase, task_id = task_id, test_id = test_id)

@app.route('/delete_task/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def deleteTask(task_id, test_id):
    if delete_task(dbase, task_id):
        flash("Задание удалено", "success")
    else:
        flash("Ошибка при удалении задания", "error")
    return redirect (url_for('showTest', test_id = test_id))

@app.route('/change_question_name/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def changeQuestionName(task_id, test_id):
    form = ChangeName()
    if form.validate_on_submit():
        if edit_task_question(dbase, task_id, form.name.data):
            flash("Название успешно изменино", "success")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
        else:
            flash("Произошла ошибка при изменении названия", "error")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
    else:
        form.name.data = dbase.get_question_by_task_id(task_id)
    return render_template('change_name.html', task_id = task_id,  form = form)

@app.route('/change_answer/<answer_id>/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def changeAnswer(answer_id, task_id, test_id):
    form = ChangeAnswerForm()
    if form.validate_on_submit():
        if edit_answer(dbase, answer_id, form.name.data, form.is_right.data):
            flash("Ответ успешно изменен", "success")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
        else:
            flash("Произошла ошибка при изменении ответа", "error")
            return redirect(url_for('editTask', answer_id = answer_id, task_id = task_id, test_id = test_id))
    else:
        res = dbase.get_answer_by_answer_id(answer_id)
        if res:
            form.name.data = res[0][0]
        form.is_right.data = res[0][1]
    
    return render_template('change_name.html', task_id = task_id,  form = form)

@app.route('/add_answer/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def addAnswer(task_id, test_id):
    form = ChangeAnswerForm()
    form.submit.label.text = "Добавить"
    if form.validate_on_submit():
        if add_answer(dbase, task_id, form.name.data, form.is_right.data):
            flash("Ответ успешно добавлен", "success")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
        else:
            flash("Произошла ошибка при добавлении ответа", "error")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
    return render_template('change_name.html', task_id = task_id,  form = form)

@app.route('/delete_task/<answer_id>/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def deleteAnswer(answer_id, task_id, test_id):
    if delete_answer(dbase, answer_id):
        flash("Ответ удален", "success")
    else:
        flash("Ошибка при удалении ответа", "error")
    return redirect(url_for('editTask', task_id = task_id, test_id = test_id))



if __name__ == "__main__":
    app.run(debug=True)
