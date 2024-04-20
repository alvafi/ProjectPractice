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
                bank_name VARCHAR(100)
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

    def add_data_bank(self, bank_name):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO TaskBank (bank_name) 
            VALUES (%s)
        ''', (bank_name,))
        self.conn.commit()
