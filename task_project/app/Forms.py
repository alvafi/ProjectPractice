from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, FileField, SelectField, IntegerField, FieldList
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed
from Config import symbol_mode, key_mode, answer_under_question_mode, XML_mode, IMS_QTI_mode

class RegisterForm(FlaskForm):
    first_name = StringField("Имя: ", validators=[DataRequired(), Length(min=1, max=20, message="Имя должно быть от 1 до 20 символов")])
    last_name = StringField("Фамилия: ", validators=[DataRequired(), Length(min=1, max=20, message="Фамилия должна быть от 1 до 20 символов")])
    middle_name = StringField("Отчество: ", validators=[Length(min=0, max=20, message="Отчество должно быть не больше 20 символов")])
    login = StringField("Логин: ", validators=[DataRequired(), Length(min=4, max=20, message="Логин должен быть от 4 до 20 символов")])
    email = StringField("Email: ", validators=[DataRequired(), Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=7, max=32, message="Пароль должен быть от 7 до 32 символов")])
    password2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    conf_flag = BooleanField("Согласие на обработку и хранение данных", validators=[DataRequired()])
    submit = SubmitField("Регистрация")

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=7, max=32, message="Пароль должен быть от 7 до 32 символов")])
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")

class UploadAvatarForm(FlaskForm):
    file = FileField("Выберите файл", validators=[FileAllowed(['png'],  message="not_png")])
    submit = SubmitField("Загрузить")

    def __init__(self, *args, **kwargs):
        super(UploadAvatarForm, self).__init__(*args, **kwargs)
        self.enctype = 'multipart/form-data'

class AddTestForm(FlaskForm):
    bank_id = SelectField("Загрузить в набор:", choices=[], validators=[DataRequired()])
    test_mode = SelectField("Формат теста:", choices=[(symbol_mode, "Символы"), (key_mode, "Ключи"), (answer_under_question_mode, "Ответы под вопросами")])
    name = StringField("Название:", validators=[DataRequired(), Length(min=1, max=20)])
    text = StringField("Введите текст", widget=TextArea(), render_kw={"maxlength": "5000"})
    file = FileField("Загрузить файл", validators=[FileAllowed(['txt', 'pdf', 'docx'],  message="not_type")])
    submit = SubmitField("Добавить")

    def __init__(self, *args, **kwargs):
        super(AddTestForm, self).__init__(*args, **kwargs)
        self.enctype = 'multipart/form-data'

class AddTestToExistingKitForm(FlaskForm):
    test_mode = SelectField("Формат теста:", choices=[(symbol_mode, "Символы"), (key_mode, "Ключи"), (answer_under_question_mode, "Ответы под вопросами")])
    name = StringField("Название:", validators=[DataRequired(), Length(min=1, max=20)])
    text = StringField("Введите текст", widget=TextArea(), render_kw={"maxlength": "3700"})
    file = FileField("Загрузить файл", validators=[FileAllowed(['txt', 'pdf', 'docx'],  message="not_type")])
    submit = SubmitField("Добавить")

    def __init__(self, *args, **kwargs):
        super(AddTestToExistingKitForm, self).__init__(*args, **kwargs)
        self.enctype = 'multipart/form-data'

class ChangeName(FlaskForm):
    name = StringField("Новое название:", validators=[Length(min=1, max=100, message="Название должно содержать от 1 до 100 символов")])
    submit = SubmitField("Изменить")

class ExportTestForm(FlaskForm):
    export_type = SelectField("Выберите формат загрузки:", choices=[(XML_mode, "MoodleXML"), (IMS_QTI_mode, "IMS QTI")])
    submit = SubmitField("Экспорт")

class ChangeAnswerForm(FlaskForm):
    name = StringField("Текст ответа:", validators=[Length(min=1, max=100, message="Ответ должен содержать от 1 до 100 символов")])
    is_right = BooleanField("Ответ правильный")
    submit = SubmitField("Изменить")

class AddTaskForm(FlaskForm):
    question = StringField("Вопрос:", validators=[Length(min=1, max=100, message="Вопрос должен содержать от 1 до 100 символов")])
    answers = FieldList(StringField("Ответ", validators=[Length(min=1, max=100, message="Ответ должен содержать от 1 до 100 символов")]))
    #is_right = FieldList(BooleanField("Ответ правильный"))
    submit = SubmitField("Добавить задание")

class NumberOfQuestionsForm(FlaskForm):
    number_of_questions = IntegerField("Количество ответов:", validators=[NumberRange(min=1, max=15)])
    submit = SubmitField("Далее")

class ChangeUserNameForm(FlaskForm):
    first_name = StringField("Имя:", validators=[Length(min=0, max=20, message="Имя должно быть не больше 20 символов")])
    last_name = StringField("Фамилия:", validators=[Length(min=0, max=20, message="Имя должно быть не больше 20 символов")])
    middle_name = StringField("Отчество:", validators=[Length(min=0, max=20, message="Имя должно быть не больше 20 символов")])
    submit = SubmitField("Изменить")