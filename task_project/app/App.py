from flask import Flask, flash, request, redirect, url_for, g, render_template, send_file, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from DB_Config import POSTGRES_DB
from database import Database
import os
from Forms import RegisterForm, LoginForm, AddTestForm, AddTestToExistingKitForm, ChangeName, ExportTestForm, ChangeAnswerForm, UploadAvatarForm, NumberOfQuestionsForm, AddTaskForm, ChangeUserNameForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import Email, Length
from UserLogin import UserLogin
from Parser import Parse
from TestClasses.Kit import Kit
from TestClasses.Task import Task
from TestClasses.Answer import Answer
from Interface import add_kit_content, delete_bank, delete_kit, edit_bank_name, edit_kit_name, edit_test_name, delete_test, add_kit_content_to_existing_kit, delete_task, edit_task_question, edit_answer, delete_answer, add_answer, resize_image, add_task_content, get_input_data
from Export import Export

DATABASE = f'/tmp/{POSTGRES_DB}.db'
SECRET_KEY = 'fc67934b56faafe32815'
MAX_CONTENT_LENGTH = 1.5 * 1024 * 1024

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(dict(DATABASE=os.path.join(app.root_path, f'{POSTGRES_DB}.db')))

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

# Загрузка данных пользователя
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

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

# Обработка ошибки 404
@app.errorhandler(404) 
def not_found(e):
    return render_template('404.html')

# Обработка ошибки 413
@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('413.html')

# Начальная страница
@app.route("/")
def start():
    if current_user.is_authenticated:
        return redirect(url_for('showBanks'))
    else:
        return render_template('main.html')

# Вход в систему
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

# Регистрация
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
                flash(res[1], "error")

    return render_template("register.html", title="Регистрация", form=form)

# Выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

# Профиль
@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

# Изменение имя/фамилия/отчество
@app.route('/change_name', methods=["POST", "GET"])
@login_required
def changeName():
    form = ChangeUserNameForm()
    if form.validate_on_submit():
        if dbase.update_user_name(current_user.get_id(), form.first_name.data, form.last_name.data, form.middle_name.data):
            flash("Имя успешно обновлено", "success")
        else:
            flash("Ошибка при обновлении имени", "error")
        return redirect(url_for('profile'))
    else:
        form.first_name.data = current_user.GetFirstName()
        form.last_name.data = current_user.GetLastName()
        form.middle_name.data = current_user.GetMiddleName()
    return render_template('change_name.html', form = form)

# Изменение email
@app.route('/change_email', methods=["POST", "GET"])
@login_required
def changeEmail():
    form = ChangeName()
    form.name.label.text = "Новый email:"
    form.name.validators = [Email("Некорректный email")]
    if form.validate_on_submit():
        res = dbase.update_user_email(current_user.get_id(), form.name.data)
        if res[0]:
            flash("Email успешно обновлен", "success")
        else:
            flash(res[1], "error")
        return redirect(url_for('profile'))
    else:
        form.name.data = current_user.GetEmail()
    return render_template('change_name.html', form = form)

# Изменение логина
@app.route('/change_login', methods=["POST", "GET"])
@login_required
def changeLogin():
    form = ChangeName()
    form.name.label.text = "Новый логин:"
    form.name.validators = [Length(min=4, max=20, message="Логин должен содержать от 4 до 20 символов")]
    if form.validate_on_submit():
        res =  dbase.update_user_login(current_user.get_id(), form.name.data)
        if res[0]:
            flash("Логин успешно обновлен", "success")
        else:
            flash(res[1], "error")
        return redirect(url_for('profile'))
    else:
        form.name.data = current_user.GetLogin()
    return render_template('change_name.html', form = form)

# Отображение аватарки
@app.route('/user_avatar')
@login_required
def userAvatar():
    img = current_user.GetAvatar()
    if not img:
        return ""
    h = make_response(bytes(img))
    h.headers['Content-Type'] = 'image/png'
    return h

# Загрузка аватрки
@app.route('/upload_avatar', methods=["POST", "GET"])
@login_required
def uploadAvatar():
    form = UploadAvatarForm()
    if form.validate_on_submit():
        if form.file.data:
            try:
                create_upload_folder()
                filename = secure_filename(form.file.data.filename)
                file_dir = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                form.file.data.save(file_dir)
                resize_image(file_dir, file_dir)
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as file:
                    img = file.read()

                res = dbase.update_user_avatar(current_user.get_id(), img)
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
                return redirect(url_for('profile'))
            except Exception:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Выберите файл", "error")
    elif form.file.errors:
        error_message = form.file.errors[0]
        if error_message == 'not_png':
            flash("Загружаемый файл должен иметь тип png", "error")

    return render_template('update_avatar.html', form = form)

# Отображение банков
@app.route('/my_banks', methods=["POST", "GET"])
@login_required
def showBanks():
    banks = dbase.get_banks_by_id(current_user.get_id())
    return render_template('show_banks.html', banks = banks, dbase = dbase)

# Добавление банка
@app.route('/add_bank', methods=["POST", "GET"])
@login_required
def addBank():
    form = ChangeName()
    form.name.label.text = "Название набора:"
    form.submit.label.text = "Создать"
    if form.validate_on_submit():
        res = dbase.add_data_bank(current_user.get_id(), form.name.data)
        if res:
            flash("Набор создан", "success")
            return redirect(url_for('showBanks'))
        else:
            flash(res[1], "error")
    return render_template('add_bank.html', form = form)

# Изменение названия банка
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
    else:
        bank_name = dbase.get_bank_name_by_bank_id(bank_id)
        if bank_name:
            form.name.data = bank_name
    return render_template('change_name.html', bank_id = bank_id,  form = form)

# Удаление банка
@app.route('/delete_bank/<bank_id>', methods=["POST", "GET"])
@login_required
def deleteBank(bank_id):
    if delete_bank(dbase, bank_id):
        flash("Набор удален", "success")
    else:
        flash("Ошибка при удалении набора", "error")
    return redirect (url_for('showBanks'))

# Изменение название набора
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
    else:
        kit_name = dbase.get_kit_name_by_kit_id(kit_id)
        if kit_name:
            form.name.data = kit_name
    return render_template('change_name.html', kit_id = kit_id, form = form)

# Загрузка теста
@app.route('/add_test', methods=["POST", "GET"])
@login_required
def addTest():
    form = AddTestForm() 
    res = dbase.get_banks_by_id(current_user.get_id())
    if res:
        form.bank_id.choices = [(bank_id, bank_name) for bank_id, bank_name in res]
    else:
        flash("Для добавления теста у вас должен быть создан хотя бы один набор", "error")
    if form.validate_on_submit():
        kit = Kit(form.name.data)
        if form.file.data:
            create_upload_folder()
            filename = secure_filename(form.file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(file_path)
            input, split_type = get_input_data(file_path, filename)   
        elif form.text.data:
            input = form.text.data
            split_type = "\\r\\n"
        else:
            flash("Введите текст или загрузите файл", "error")
            return(redirect(url_for('addTest')))
        
        if not(Parse(form.name.data, input, kit, form.test_mode.data, split_type)):
                flash("Ошибка при обработке теста", "error")
                return(redirect(url_for('addTest')))

        if add_kit_content(dbase, kit, form.bank_id.data):
            flash("Тест добавлен", "success")
        else:
            flash("Произошла ошибка при добавлении теста", "error")
        return redirect(url_for('showBanks'))
    
    elif form.file.errors:
        error_message = form.file.errors[0]
        if error_message == 'not_type':
            flash("Загружаемый файл должен иметь тип txt, pdf или docx", "error")
    return render_template('add_test.html', title = "Добавление теста", form = form)

# Загрузка и добавление теста в существующий набор
@app.route('/add_test_to_kit/<kit_id>', methods=["POST", "GET"])
@login_required
def addTestToExistingKit(kit_id):
    form = AddTestToExistingKitForm() 
    if form.validate_on_submit():
        kit = Kit(form.name.data)
        if form.file.data:
            create_upload_folder()
            filename = secure_filename(form.file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(file_path)
            input, split_type = get_input_data(file_path, filename)   
        elif form.text.data:
            input = form.text.data
            split_type = "\\r\\n"
        else:
            flash("Введите текст или загрузите файл", "error")
            return redirect(url_for('addTestToExistingKit', kit_id = kit_id))
        
        if not(Parse(form.name.data, input, kit, form.test_mode.data, split_type)):
                flash("Ошибка при обработке теста", "error")
                return redirect(url_for('addTestToExistingKit', kit_id = kit_id))
        
        if add_kit_content_to_existing_kit(dbase, kit, kit_id):
            flash("Тест добавлен", "success")
        else:
            flash("Произошла ошибка при добавлении теста", "error")
        return redirect(url_for('showBanks'))
    
    elif form.file.errors:
        error_message = form.file.errors[0]
        if error_message == 'not_type':
            flash("Загружаемый файл должен иметь тип txt, pdf или docx", "error")
    return render_template('add_test_to_existing_kit.html', title = "Добавление теста", form = form, kit_id = kit_id)

# Изменение названия набора
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
    else:
        test_name = dbase.get_test_name_by_test_id(test_id)
        if test_name:
            form.name.data = test_name
    return render_template('change_name.html', test_id = test_id, form = form)

# Удаление набора
@app.route('/delete_kit/<kit_id>', methods=["POST", "GET"])
@login_required
def deleteKit(kit_id):
    if delete_kit(dbase, kit_id):
        flash("Тесты удалены", "success")
    else:
        flash("Ошибка при удалении тестов", "error")
    return redirect (url_for('showBanks'))

# Экспорт теста
@app.route('/export_test/<test_id>', methods=["POST", "GET"])
@login_required
def exportTest(test_id):
    form = ExportTestForm()
    if form.validate_on_submit():
        data = Export(dbase, test_id, form.export_type.data)
        if data:
            test_name = dbase.get_test_name_by_test_id(test_id)
            if not test_name:
                test_name = "test"
            flash("Тест успешно экспортирован", "success")
            return send_file(data, as_attachment=True, download_name=str(test_name + '.' +  form.export_type.data))
        else:
            flash("Произошла ошибка при экспорте теста", "error")
            return redirect(url_for('showBanks'))
    return render_template("export_test.html", form = form)

# Отображение теста
@app.route('/show_test/<test_id>', methods=["POST", "GET"])
@login_required
def showTest(test_id):
    res = dbase.get_tasks_by_test_id(test_id)
    return render_template('show_tests.html', dbase = dbase, tasks = res, test_id = test_id)

# Удаление теста
@app.route('/delete_test/<test_id>', methods=["POST", "GET"])
@login_required
def deleteTest(test_id):
    if delete_test(dbase, test_id):
        flash("Тест удален", "success")
    else:
        flash("Ошибка при удалении теста", "error")
    return redirect (url_for('showBanks'))

# Форма для количества ответов при добавлении задания
@app.route('/add_task/<test_id>', methods=["POST", "GET"])
@login_required
def addTask(test_id):
    form = NumberOfQuestionsForm()
    if form.validate_on_submit():
        return redirect(url_for("addDataTask", number_of_questions = form.number_of_questions.data, test_id = test_id))
    return render_template('add_task.html', test_id = test_id, form = form)

# Ручное добавление задания в тест
@app.route('/add_data_task/<int:number_of_questions>/<test_id>', methods=["POST", "GET"])
@login_required
def addDataTask(number_of_questions, test_id):
    form = AddTaskForm()
    while len(form.answers) < number_of_questions:
        form.answers.append_entry()

    if form.validate_on_submit():
        answers = []
        for i in range(len(form.answers.entries)):
            answers.append(Answer(form.answers.entries[i].data, False))
        task = Task(form.question.data, answers)
        if add_task_content(dbase, task, test_id):
            flash("Задание успешно добавлено", "success")
        else:
            flash("Произошла ошибка при добавлении задания", "error")
        return redirect(url_for("showTest", test_id = test_id))
    return render_template('add_data_task.html', test_id = test_id, number_of_questions = number_of_questions, form = form)

# Редактирование задания
@app.route('/edit_task/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def editTask(task_id, test_id):
    return render_template('show_task.html', dbase = dbase, task_id = task_id, test_id = test_id)

# Удаление задания
@app.route('/delete_task/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def deleteTask(task_id, test_id):
    if delete_task(dbase, task_id):
        flash("Задание удалено", "success")
    else:
        flash("Ошибка при удалении задания", "error")
    return redirect (url_for('showTest', test_id = test_id))

# Изменения текста вопроса
@app.route('/change_question_name/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def changeQuestionName(task_id, test_id):
    form = ChangeName()
    form.name.label.text = "Вопрос:"
    form.submit.label.text = "Изменить"
    if form.validate_on_submit():
        if edit_task_question(dbase, task_id, form.name.data):
            flash("Вопрос успешно изменен", "success")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
        else:
            flash("Произошла ошибка при изменении вопроса", "error")
            return redirect(url_for('editTask', task_id = task_id, test_id = test_id))
    else:
        form.name.data = dbase.get_question_by_task_id(task_id)
    return render_template('change_name.html', task_id = task_id,  form = form)

# Изменения текста ответа
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

# Добавление ответа
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

# Удаление ответа
@app.route('/delete_answer/<answer_id>/<task_id>/<test_id>', methods=["POST", "GET"])
@login_required
def deleteAnswer(answer_id, task_id, test_id):
    if delete_answer(dbase, answer_id):
        flash("Ответ удален", "success")
    else:
        flash("Ошибка при удалении ответа", "error")
    return redirect(url_for('editTask', task_id = task_id, test_id = test_id))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8080")