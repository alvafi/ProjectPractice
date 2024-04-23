# Тут импорт всех муодулей: хэширование, модуль для работы с файлами на компьюетере(в init_file используется)
import hashlib
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
Объясняю:
login: str требует, чтобы в функцию передалась только строка.
-> bool говорит о том, что функция возвращает значение типа bool.
Комментарий под функцией добавляет ее описание в подсказки(в pycharm точно добавляеь), да и просто так легче понимать.
Хэширование надо для того, чтобы никто не смог зайти в файл и узнать все пароли, это как бонус к этому примеру.
"""


def init_file():  # Инициализация файла, если этого не сделать програма вылетит м ошибкой, что файла нет
    """Создает файл пользователей"""
    if not os.path.exists('users.txt'):
        with open('users.txt', 'w'):
            pass


def add_user(second_name: str, first_name: str, middle_name: str, email_address: str, login: str, password: str) -> bool:
    """Добавляет пользователя в файл"""
    with open('users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла
    for user in users:
        args = user.split(':')
        if login == args[4]:  # Если логин уже есть, парль не проверяем, шанс взлома увеличится(кто-то мб узнает пароль)
            return False  # Тут можно написать что угодно, будь то HTML статус(409 - conflict), либо просто фразу ошибки
        
    with open('users.txt', 'a') as f:
        f.write(f'{second_name}:{first_name}:{middle_name}:{email_address}:{login}:{password}\n')  # Добавляем нового пользователя
    return True


def get_user(login: str, password: str) -> bool:
    """Проверяет логин и пароль пользователя"""
    with open('users.txt', 'r') as f:
        users = f.read().splitlines()  # Считываем всех пользователей из файла

    for user in users:
        args = user.split(':')
        if login == args[4] and password == args[5]:  # Если пользователь с таким логином и паролем существует
            return True
    return False


def main_loop(login: str):
    """Главный цикл программы"""
    print(f'Привет, {login}!')  # Тут основная часть программы


init_file()

while True:
    print('''Добро пожаловать! Выберите пункт меню:
    1. Вход
    2. Регистрация
    3. Выход''')

    user_input = input()
    if user_input == '2':  # Условия можно заменить на: user_input.lower() == 'вход'
        print('Введите логин:')
        login = input()

        print('Введите пароль:')
        password = input()

        print('Повторно введите пароль:')
        password_repeat = input()

        print('Введите Фамилию:')
        second_name = input()

        print('Введите Имя:')
        first_name = input()

        print('Введите Отчество:')
        middle_name = input()

        print ('Введите почту')
        email_address = input()

        if password!=password_repeat:
            print("Пароли не совпадают")

        else:
            addressToVerify = email_address
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

            if match == None:
                print('Bad Syntax in ' + addressToVerify)
                raise ValueError('Bad Syntax')

            # Настройки почтового сервера
            smtp_server_gmail = 'smtp.gmail.com'
            port= 465
            sender_email = 'melnikonmymind@gmail.com'
            sender_password = 'gpqp cvvv kajj iske'

            # Получатель и тема письма
            recipient_email = email_address
            subject = 'Подтверждение почты'

            # Текст письма
            message = 'Добрый день, ваш адрес электронной почты был успешно подтвержден.'

            # Создаем сообщение
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Подключаемся к почтовому серверу и отправляем письмо
            
            with smtplib.SMTP_SSL(smtp_server_gmail, port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                result = get_user(login, hashlib.sha256(password.encode()).hexdigest())
            
            result = add_user(second_name, first_name, middle_name, email_address, login, hashlib.sha256(password.encode()).hexdigest())  # Вызываем функцию добавления пользователя. И хешируем пароль(безопасность)
            if not result:
                print('Пользователь с таким логином уже существует')
            else:
                print('Регистрация прошла успешно!')
    elif user_input == '1':
        print('Введите логин:')
        login = input()

        print('Введите пароль:')
        password = input()

        result = get_user(login, hashlib.sha256(password.encode()).hexdigest())  # Вызываем функцию добавления пользователя. И хешируем пароль(безопасность)
        if result == True:
            print('Всё ок')
        else:
            print('Чет накосячил')

    elif user_input == '3':
        print('Завершение работы')
        break  # Выходим из цикла