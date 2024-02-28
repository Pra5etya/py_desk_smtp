import sqlite3

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, password TEXT, email TEXT)''')
        self.conn.commit()

    def register_user(self, username, password, email):
        c = self.conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        self.conn.commit()

    def login_user(self, username, password):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return c.fetchone()

    def find_user_by_email(self, email):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        return c.fetchone()

    def update_password(self, email, new_password):
        c = self.conn.cursor()
        c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
        self.conn.commit()
