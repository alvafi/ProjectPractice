from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

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
    submit = SubmitField("Регистрация")