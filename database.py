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
            CREATE TABLE IF NOT EXISTS TaskBank (
                bank_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                bank_name VARCHAR(100),
                FOREIGN KEY (user_id) REFERENCES "User" (user_id)
            )
        ''')
        self.conn.commit()

    def add_data_user(self, last_name, first_name, middle_name, login, email, password):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO "User" (last_name, first_name, middle_name, email, login, password) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (last_name, first_name, middle_name, email, login, password))
        self.conn.commit()


    def add_data_bank(self, user_id, bank_name):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO TaskBank (user_id, bank_name) 
            VALUES (%s, %s)
        ''', (user_id, bank_name,))
        self.conn.commit()

