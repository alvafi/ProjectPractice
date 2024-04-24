import psycopg2
import config as cfg

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(database=cfg.db_name, user=cfg.db_user, host=cfg.db_host, password=cfg.db_password)

    def create_db(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS "User" (
                user_id SERIAL PRIMARY KEY,
                last_name VARCHAR(20),
                first_name VARCHAR(20),
                middle_name VARCHAR(20),
                email VARCHAR(200) NOT NULL UNIQUE,
                login VARCHAR(200) NOT NULL UNIQUE,
                password VARCHAR(100)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Bank (
                bank_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                bank_name VARCHAR(100),
                FOREIGN KEY (user_id) REFERENCES "User" (user_id) ON DELETE CASCADE
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Kit (
                kit_id SERIAL PRIMARY KEY,
                bank_id INTEGER,
                kit_name VARCHAR(100),
                FOREIGN KEY (bank_id) REFERENCES Bank (bank_id) ON DELETE CASCADE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Test (
                test_id SERIAL PRIMARY KEY,
                kit_id INTEGER,
                test_name VARCHAR(100),
                FOREIGN KEY (kit_id) REFERENCES Kit (kit_id) ON DELETE CASCADE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Task (
                task_id SERIAL PRIMARY KEY,
                kit_id INTEGER,
                test_id INTEGER,
                question_text VARCHAR(1000),
                FOREIGN KEY (kit_id) REFERENCES Kit (kit_id) ON DELETE CASCADE,
                FOREIGN KEY (test_id) REFERENCES Test (test_id) ON DELETE CASCADE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Answer (
                answer_id SERIAL PRIMARY KEY,
                task_id INTEGER,
                answer_text VARCHAR(1000),
                is_right BOOLEAN,
                FOREIGN KEY (task_id) REFERENCES Task (task_id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()

    def add_data_user(self, last_name, first_name, middle_name, login, email, password):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO "User" (last_name, first_name, middle_name, email, login, password) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING user_id
        ''', (last_name, first_name, middle_name, email, login, password))
        self.conn.commit()
        return cur.fetchone()[0]

    def add_data_bank(self, user_id: int, bank_name: str):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO Bank (user_id, bank_name) 
            VALUES (%s, %s) 
            RETURNING bank_id
        ''', (user_id, bank_name,))
        self.conn.commit()
        return cur.fetchone()[0]

    def add_data_kit(self, bank_id: int, kit_name: str):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO Kit (bank_id, kit_name) 
            VALUES (%s, %s) 
            RETURNING kit_id
        ''', (bank_id, kit_name,))
        self.conn.commit()
        return cur.fetchone()[0]

    def add_data_test(self, kit_id: int, test_name: str):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO Test (kit_id, test_name)
            VALUES (%s, %s) 
            RETURNING test_id
        ''', (kit_id, test_name,))
        self.conn.commit()
        return cur.fetchone()[0]

    def add_data_task(self, kit_id: int, test_id: int, question_text: str):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO Task (kit_id, test_id, question_text)
            VALUES (%s, %s, %s) 
            RETURNING task_id
        ''', (kit_id, test_id, question_text,))
        self.conn.commit()
        return cur.fetchone()[0]

    def add_data_answer(self, task_id: int, answer_text: str, is_right: bool):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO Answer (task_id, answer_text, is_right)
            VALUES (%s, %s, %s) 
            RETURNING answer_id
        ''', (task_id, answer_text, is_right,))
        self.conn.commit()
        return cur.fetchone()[0]

    def update_bank_name(self, user_id: int, bank_id: int, new_bank_name: str):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE Bank 
            SET bank_name = %s 
            WHERE user_id = %s AND bank_id = %s
        ''', (new_bank_name, user_id, bank_id,))
        self.conn.commit()

    def update_kit_name(self, kit_id: int, new_bank_name: str):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE Kit 
            SET kit_name = %s 
            WHERE kit_id = %s
        ''', (new_bank_name, kit_id))
        self.conn.commit()

    def update_test_name(self, test_id: int, new_test_name: str):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE Test 
            SET test_name = %s 
            WHERE test_id = %s
        ''', (new_test_name, test_id))
        self.conn.commit()

    def update_test_question(self, task_id: int, new_task_question: str):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE Task 
            SET question_text = %s 
            WHERE task_id = %s
        ''', (new_task_question, task_id))
        self.conn.commit()

    def update_answer(self, answer_id: int, new_answer_text: str, is_right: bool):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE Answer 
            SET answer_text = %s, is_right = %s 
            WHERE answer_id = %s
        ''', (new_answer_text, is_right, answer_id))
        self.conn.commit()

    def delete_data_user(self, user_id: int):
        cur = self.conn.cursor()
        cur.execute('''
               DELETE 
               FROM "User" 
               WHERE user_id = %s
           ''', (user_id,))
        self.conn.commit()

    def delete_data_bank(self, bank_id: int):
        cur = self.conn.cursor()
        cur.execute('''
               DELETE 
               FROM Bank 
               WHERE bank_id = %s
           ''', (bank_id,))
        self.conn.commit()

    def delete_data_kit(self, kit_id: int):
        cur = self.conn.cursor()
        cur.execute('''
            DELETE 
            FROM Kit 
            WHERE kit_id = %s
        ''', (kit_id,))
        self.conn.commit()

    def delete_data_test(self, test_id: int):
        cur = self.conn.cursor()
        cur.execute('''
            DELETE 
            FROM Test 
            WHERE test_id = %s
        ''', (test_id,))
        self.conn.commit()

    def delete_data_task(self, task_id: int):
        cur = self.conn.cursor()
        cur.execute('''
            DELETE
            FROM Task 
            WHERE task_id = %s
        ''', (task_id,))
        self.conn.commit()

    def delete_data_answer(self, answer_id: int):
        cur = self.conn.cursor()
        cur.execute('''
            DELETE 
            FROM Answer 
            WHERE answer_id = %s
        ''', (answer_id,))
        self.conn.commit()
