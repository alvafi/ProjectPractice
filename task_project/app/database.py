import psycopg2
import sqlite3
import DB_Config as cfg

class Database:
    def __init__(self):
        self.__conn = psycopg2.connect(database = cfg.POSTGRES_DB, user = cfg.POSTGRES_USER,  password = cfg.POSTGRES_PASSWORD, host = cfg.POSTGRES_HOST)
        self.create_db()

    def create_db(self):
        cur = self.__conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id BIGSERIAL PRIMARY KEY,
                last_name text NOT NULL,
                first_name text NOT NULL,
                middle_name text,
                email text NOT NULL UNIQUE,
                login text NOT NULL UNIQUE,
                password text NOT NULL,
                avatar BYTEA DEFAULT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Bank (
                bank_id BIGSERIAL PRIMARY KEY,
                user_id BIGINT,
                bank_name VARCHAR(100),
                FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Kit (
                kit_id BIGSERIAL PRIMARY KEY,
                bank_id BIGINT,
                kit_name VARCHAR(100),
                FOREIGN KEY (bank_id) REFERENCES Bank (bank_id) ON DELETE CASCADE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Test (
                test_id BIGSERIAL PRIMARY KEY,
                kit_id BIGINT,
                test_name VARCHAR(100),
                FOREIGN KEY (kit_id) REFERENCES Kit (kit_id) ON DELETE CASCADE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Task (
                task_id BIGSERIAL PRIMARY KEY,
                kit_id BIGINT,
                test_id BIGINT,
                question_text VARCHAR(1000),
                FOREIGN KEY (kit_id) REFERENCES Kit (kit_id) ON DELETE CASCADE,
                FOREIGN KEY (test_id) REFERENCES Test (test_id) ON DELETE SET NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Answer (
                answer_id BIGSERIAL PRIMARY KEY,
                task_id BIGINT,
                answer_text VARCHAR(1000),
                is_right BOOLEAN,
                FOREIGN KEY (task_id) REFERENCES Task (task_id) ON DELETE CASCADE
            )
        ''')

        self.__conn.commit()

    def add_data_user(self, last_name, first_name, middle_name, email, login, password):
        try:
            cur = self.__conn.cursor()

            cur.execute(f"SELECT COUNT(*) as email_count FROM Users WHERE email LIKE '{email}'")
            res = cur.fetchone()
            if res[0] > 0:
                return (False, "Пользователь с таким email уже существует")
            
            cur.execute(f"SELECT COUNT(*) as login_count FROM Users WHERE login LIKE '{login}'")
            res = cur.fetchone()
            if res[0] > 0:
                print()
                return (False, "Пользователь с таким login уже существует")

            cur.execute('''
                INSERT INTO Users (last_name, first_name, middle_name, email, login, password) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                RETURNING user_id
            ''', (last_name, first_name, middle_name, email, login, password))
            self.__conn.commit()

        except sqlite3.Error as e:
            return (False, "Произошла ошибка при обработке формы")

        return (True, '')
    
    def add_data_bank(self, user_id: int, bank_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO Bank (user_id, bank_name) 
                VALUES (%s, %s) 
                RETURNING bank_id
            ''', (user_id, bank_name,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return None, str(e)

        return cur.fetchone()[0], ""

    def add_data_kit(self, bank_id: int, kit_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO Kit (bank_id, kit_name) 
                VALUES (%s, %s) 
                RETURNING kit_id
            ''', (bank_id, kit_name,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return None, str(e)

        return cur.fetchone()[0], ""

    def add_data_test(self, kit_id: int, test_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO Test (kit_id, test_name)
                VALUES (%s, %s) 
                RETURNING test_id
            ''', (kit_id, test_name,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return None, str(e)

        return cur.fetchone()[0], ""

    def add_data_task(self, kit_id: int, test_id, question_text: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO Task (kit_id, test_id, question_text)
                VALUES (%s, %s, %s) 
                RETURNING task_id
            ''', (kit_id, test_id, question_text,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return None, str(e)

        return cur.fetchone()[0], ""

    def add_data_answer(self, task_id: int, answer_text: str, is_right: bool):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO Answer (task_id, answer_text, is_right)
                VALUES (%s, %s, %s) 
                RETURNING answer_id
            ''', (task_id, answer_text, is_right,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return None, str(e)

        return cur.fetchone()[0], ""
    
    def update_user_name(self, user_id, first_name : str, last_name: str, middle_name : str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                UPDATE Users
                SET last_name = %s, first_name = %s, middle_name = %s
                WHERE user_id = %s
            ''', (last_name, first_name, middle_name, user_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False
        return True
    
    def update_user_email(self, user_id, email : str):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT COUNT(*) as email_count FROM Users WHERE email LIKE '{email}'")
            res = cur.fetchone()
            if res[0] > 0:
                return (False, "Пользователь с таким email уже существует")

            cur.execute('''
                UPDATE Users
                SET email = %s
                WHERE user_id = %s
            ''', (email, user_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return (False, "Ошибка при обработке email")
        return (True, '')
    
    def update_user_login(self, user_id, login : str):
        try:
            cur = self.__conn.cursor()   
            cur.execute(f"SELECT COUNT(*) as login_count FROM Users WHERE login LIKE '{login}'")
            res = cur.fetchone()
            if res[0] > 0:
                print()
                return (False, "Пользователь с таким login уже существует")

            cur.execute('''
                UPDATE Users
                SET login = %s
                WHERE user_id = %s
            ''', (login, user_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return (False, "Ошибка при обработке login")
        return (True, '')

    def update_bank_name(self, bank_id: int, new_bank_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                UPDATE Bank 
                SET bank_name = %s
                WHERE bank_id = %s
            ''', (new_bank_name, bank_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def update_kit_name(self, kit_id: int, new_bank_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                UPDATE Kit 
                SET kit_name = %s 
                WHERE kit_id = %s
            ''', (new_bank_name, kit_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def update_test_name(self, test_id: int, new_test_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                UPDATE Test 
                SET test_name = %s 
                WHERE test_id = %s
            ''', (new_test_name, test_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def update_task_question(self, task_id: int, new_task_question: str):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                UPDATE Task 
                SET question_text = %s 
                WHERE task_id = %s
            ''', (new_task_question, task_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def update_task_tests_id(self, tasks_id, new_test_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute(f'''
                UPDATE Task
                SET test_id = '{new_test_id}'
                WHERE task_id in ({','.join(str(i) for i in tasks_id)})
            ''')
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def update_answer(self, answer_id: int, new_answer_text: str, is_right: bool):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                UPDATE Answer 
                SET answer_text = %s, is_right = %s 
                WHERE answer_id = %s
            ''', (new_answer_text, is_right, answer_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def delete_data_user(self, user_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                   DELETE 
                   FROM Users
                   WHERE user_id = %s
               ''', (user_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def delete_data_bank(self, bank_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                   DELETE 
                   FROM Bank 
                   WHERE bank_id = %s
               ''', (bank_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def delete_data_kit(self, kit_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                DELETE 
                FROM Kit 
                WHERE kit_id = %s
            ''', (kit_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def delete_data_test(self, test_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                DELETE 
                FROM Test 
                WHERE test_id = %s
            ''', (test_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def delete_data_task(self, task_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                DELETE
                FROM Task 
                WHERE task_id = %s
            ''', (task_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def delete_data_answer(self, answer_id: int):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                DELETE 
                FROM Answer 
                WHERE answer_id = %s
            ''', (answer_id,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False, str(e)

        return True, ""

    def get_user_avatar(self, user_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT avatar FROM Users WHERE user_id = {user_id} LIMIT 1")
            res = cur.fetchone()
            if not res:
                return False
            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    
    def update_user_avatar(self, user_id, avatar):
        try:
            binary = sqlite3.Binary(avatar)
            cur = self.__conn.cursor()
            cur.execute(f"UPDATE Users SET avatar = %s WHERE user_id = %s", (binary, user_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False
        return True

    def get_user_by_id(self, user_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT * FROM Users WHERE user_id = {user_id} LIMIT 1")
            res = cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            user_dict = {
            "user_id": res[0],
            "last_name": res[1],
            "first_name": res[2],
            "middle_name": res[3],
            "email": res[4],
            "login": res[5],
            "password": res[6],
            "avatar" : res[7]
            }
            return user_dict
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_user_by_email(self, email):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT * FROM Users WHERE email = '{email}' LIMIT 1")
            res = cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            user_dict = {
            "user_id": res[0],
            "last_name": res[1],
            "first_name": res[2],
            "middle_name": res[3],
            "email": res[4],
            "login": res[5],
            "password": res[6],
            "avatar" : res[7]
            }
            return user_dict
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False
    
    def get_banks_by_id(self, user_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT bank_id, bank_name FROM Bank WHERE user_id = {user_id}  ORDER BY bank_id")
            res = cur.fetchall()
            if not res:
                return False

            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_kits_by_bank_id(self, bank_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT kit_id, kit_name FROM Kit WHERE bank_id = {bank_id}  ORDER BY kit_id")
            res = cur.fetchall()
            if not res:
                return False

            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    
    def get_tests_by_kit_id(self, kit_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT test_id, test_name FROM Test WHERE kit_id = {kit_id} ORDER BY test_id")
            res = cur.fetchall()
            if not res:
                return False

            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_kit_id_by_test_id(self, test_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT kit_id FROM Test WHERE test_id = {test_id} LIMIT 1 ORDER BY kit_id")
            res = cur.fetchall()
            if not res:
                return False
            return res[0][0]
        except sqlite3.Error as e:
            return False

    def get_tasks_by_test_id(self, test_id):
        try:
            cur = self.__conn.cursor()
            if test_id is None:
                cur.execute(f"SELECT task_id, question_text FROM Task WHERE test_id IS NULL")
            else:
                cur.execute(f"SELECT task_id, question_text FROM Task WHERE test_id = {test_id}")

            res = cur.fetchall()
            if not res:
                return False

            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_tasks_by_kit_id_where_test_id_is_null(self, kit_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT task_id, question_text FROM Task WHERE kit_id = {kit_id} AND test_id is NULL ORDER BY task_id")
            res = cur.fetchall()
            if not res:
                return False

            return res

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
    
    def get_answers_by_task_id(self, task_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT answer_id, answer_text, is_right FROM Answer WHERE task_id = {task_id} ORDER BY answer_id")
            res = cur.fetchall()
            if not res:
                return False

            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False
    
    def get_test_name_by_test_id(self, test_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT test_name FROM Test WHERE test_id = {test_id}")
            res = cur.fetchall()
            if not res:
                return False

            return res[0][0]
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_bank_name_by_bank_id(self, bank_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT bank_name FROM Bank WHERE bank_id = {bank_id}")
            res = cur.fetchall()
            if not res:
                return False

            return res[0][0]
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def get_kit_name_by_kit_id(self, kit_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT kit_name FROM Kit WHERE kit_id = {kit_id}")
            res = cur.fetchall()
            if not res:
                return False

            return res[0][0]
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False
    
    def get_question_by_task_id(self, task_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT question_text FROM Task WHERE task_id = {task_id}")
            res = cur.fetchall()
            if not res:
                return False

            return res[0][0]
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False
    
    def get_answer_by_answer_id(self, answer_id):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT answer_text, is_right FROM Answer WHERE answer_id = {answer_id}")
            res = cur.fetchall()
            if not res:
                return False

            return res
        
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def SetConn(self):
        self.__conn = self.__conn = psycopg2.connect(database=cfg.db_name, user=cfg.db_user, host=cfg.db_host, password=cfg.db_password)
        return self.__conn

    def Close(self):
        return self.__conn.close()
