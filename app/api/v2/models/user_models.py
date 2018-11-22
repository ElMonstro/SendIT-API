import os
from werkzeug.security import check_password_hash
from app.db_config import get_connection
import psycopg2
from flask import current_app as app 
from app.api.v2.utils.validators import Validator
from app.db_config import DbConnect


# Admin statuses
admin = True
not_admin = False

class DataBase:
    """Initialize  database classes"""
    def __init__(self):
        url = app.config['DB_URL']
        self.conn = get_connection(url)
        self.cursor = self.conn.cursor()
        self.validators = Validator()

    def __del__(self):
        """destroy object"""
        self.cursor.close()
        self.conn.close()


class Users(DataBase):
    """Handles user table db operations"""
    def add_user(self,user_dict):
        """Inserts user data into user table"""      
        query = """INSERT INTO users (username, password, email)
                VALUES ('{username}', '{password}', '{email}') RETURNING user_id;""".format(**user_dict)
        self.cursor.execute(query)
        self.conn.commit()     
        return self.cursor.fetchone()[0]

    def get_user(self, username):
        query = """SELECT  user_id, username, email, is_admin FROM users WHERE username = '{}';""".format(username)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        user_dict = {user[0]: [user[1], user[2], user[3]],}
        return user_dict

    def get_all_username_emails(self):
        """Fetches all usernames and emails"""
        query = """SELECT username, email FROM users;"""
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        user_dict = {'usernames': [], 'emails': []}
        if users:
            for user in users:
                user_dict['usernames'].append(user[0])
                user_dict['emails'].append(user[1])
        return user_dict

    def check_password(self, username, password):
        """Check if credentials are right"""
        query = """SELECT  password FROM users WHERE username = '{}';""".format(username)
        self.cursor.execute(query)
        pwd = self.cursor.fetchone()[0]        
        return check_password_hash(pwd, password)        

    def get_user_id(self, username):
        """Check if user is there"""
        query = """SELECT  user_id FROM users WHERE username = '{}';""".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def is_admin(self, user_id):
        """check if user is an admin"""
        query = """SELECT is_admin FROM users WHERE user_id = {}""".format(user_id)
        self.cursor.execute(query)
        admin = self.cursor.fetchone()
        return admin[0]
    
    
