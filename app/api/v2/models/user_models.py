import os
from app.db_config import get_connection
import psycopg2
from flask import current_app as app 
from app.api.v2.utils.validators import Validator


# Admin statuses
admin = True
not_admin = False

class DataBase:
    """Initialize  database classes"""
    def __init__(self):
        self.conn = get_connection(os.getenv('DB_URL'))
        self.cursor = self.conn.cursor()
        self.validators = Validator()


class Users(DataBase):
    """Handles user table db operations"""
    def add_user(self,user_dict):
        """Inserts user data into user table"""
        is_succesful = True        
        query = """INSERT INTO users (username, password, email)
                VALUES ('{username}', '{password}', '{email}');""".format(**user_dict)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.IntegrityError:
            is_succesful = False
        return is_succesful



    def get_user(self, username):
        query = """SELECT  user_id, username, email, is_admin FROM users WHERE username = {};""".format(username)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        user_dict = {user[0]: [user[1], user[2], user[3]],}
        return user_dict
       

    def get_all_users(self):
        """Gets all users"""
        query = """SELECT user_id, username, email, is_admin FROM users;"""
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        users_dict = {}
        if users:
            for user in users:
                users_dict[user[0]] = [user[1], user[2], user[3]]
        return users_dict


    def check_password(self, username, password):
        """Check if credentials are right"""
        query = """SELECT  password FROM users WHERE username = '{}';""".format(username)
        self.cursor.execute(query)
        pwd = self.cursor.fetchone()        
        return password == pwd[0]
        
        

    def is_user_there(self, username):
        """Check if user is there"""
        is_there = True
        query = """SELECT  password FROM users WHERE username = '{}';""".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if not result:
            is_there = False
        return is_there

    def create_admin(self):
        """Creates admin"""    
        query = """INSERT INTO users (username, password, email, is_admin)
                VALUES ('admin', 'password', 'jratcher@gmail.com', True);"""
        self.cursor.execute(query)
        self.conn.commit()

    def is_admin(self, username):
        """check if user is an admin"""
        query = """SELECT is_admin FROM users WHERE username = '{}'""".format(username)
        self.cursor.execute(query)
        return self.cursor.fetchone[0]
    


class Notification(DataBase):
    """Handles notification table operations"""
    def get_user_notifications(self, id):
        pass

    def get_admin_notifications(self):
        pass
