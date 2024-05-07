from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed, FileRequired
from Config import symbol_mode, key_mode, answer_under_question_mode


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=7, max=100, message="Пароль должен быть от 7 до 100 символов")])
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    first_name = StringField("Имя: ", validators=[Length(min=0, max=20, message="Имя должно быть не больше 20 символов")])
    last_name = StringField("Фамилия: ", validators=[Length(min=0, max=20, message="Фамилия должно быть не больше 20 символов")])
    middle_name = StringField("Отчество: ", validators=[Length(min=0, max=20, message="Отчество должно быть не больше 20 символов")])
    login = StringField("Логин: ", validators=[Length(min=4, max=200, message="Логин должен быть от 4 до 200 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=7, max=100, message="Пароль должен быть от 7 до 100 символов")])
    password2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    conf_flag = BooleanField("Согласие на обработку и хранение данных", validators=[DataRequired()])
    submit = SubmitField("Регистрация")

class AddTaskForm(FlaskForm):
    bank_id = SelectField("Загрузить в набор:", choices=[], validators=[DataRequired(message="Для добавления теста у вас должен быть создан хотя бы один набор")])
    test_mode = SelectField("Формат теста:", choices=[(symbol_mode, "Символы"), (key_mode, "Ключи"), (answer_under_question_mode, "Ответы под вопросами")])
    name = StringField("Название:", validators=[Length(min=1, max=200, message="Название должно содержать от 1 до 200 символов")])
    text = StringField("Введите текст", widget=TextArea())
    file = FileField("Загрузить файл")
    submit = SubmitField("Добавить")

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.enctype = 'multipart/form-data'

class AddBankForm(FlaskForm):
    name = StringField("Название набора:", validators=[Length(min=1, max=200, message="Название должно содержать от 1 до 200 символов")])
    submit = SubmitField("Создать")

class ChangeName(FlaskForm):
    name = StringField("Новое название:", validators=[Length(min=1, max=200, message="Название должно содержать от 1 до 200 символов")])
    submit = SubmitField("Изменить")