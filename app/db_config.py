import os
import psycopg2


class DbConnect:
    def __init__(self, config='dev'):
        if config == 'test':
            self.DB_URL = os.getenv('TEST_DB_URL')
        if config == 'dev':
            self.DB_URL = 'postgres://gjmfftiqogkmro:094234a259032a6aa229e5b2680d98f5c582ade219feac97b263f360010dc709@ec2-54-204-36-249.compute-1.amazonaws.com:5432/d1csuju2i60r9m'
        self.config = config
        self.conn = get_connection(self.DB_URL)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create tabes"""
        queries = create_queries()
        if self.config == 'dev':
            queries.pop()
        try:
            for query in queries:
                self.cursor.execute(query)
        except psycopg2.IntegrityError:
            pass
        self.conn.commit()
    
    def get_last_record_id(self):
        """Retuns the last record id"""
        query = """SELECT order_id FROM orders order by order_id desc limit 1;"""
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def delete_all_orders(self):
        """Delete all from all"""
        query = """DELETE FROM orders"""
        self.cursor.execute(query)
        self.conn.commit()
    
    def delete_latest_user(self):
        """Delete latest user"""
        query = """SELECT user_id FROM users order by user_id desc limit 1;"""
        self.cursor.execute(query)
        user_id = self.cursor.fetchone()[0]
        query = """DELETE FROM users WHERE user_id = {};""".format(user_id)
        self.cursor.execute(query)
        self.conn.commit()
    

def get_connection(url):
    """Creates and return connection"""
    conn = psycopg2.connect(url)
    return conn

def create_queries():
    """Return queries"""
    user_table = """
        CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        username VARCHAR (100) UNIQUE NOT NULL,
        password VARCHAR (50) NOT NULL,
        email VARCHAR (355) UNIQUE NOT NULL,
        is_admin BOOL DEFAULT FALSE,
        created_on TIMESTAMP DEFAULT NOW(),
        last_login TIMESTAMP
        );"""

    order_table = """
        CREATE TABLE IF NOT EXISTS  orders (
        order_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id) ,
        recepient_name VARCHAR (355) NOT NULL,
        recepient_no INTEGER NOT NULL,        
        pickup VARCHAR (50) NOT NULL,
        current_location VARCHAR (50),
        dest VARCHAR (50) NOT NULL,
        weight INTEGER NOT NULL,
        status VARCHAR (12) DEFAULT 'In-transit',
        created_on TIMESTAMP DEFAULT NOW()
        );"""

    notifications = """
        CREATE TABLE IF NOT EXISTS notifications(
        notification_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users,
        order_id INTEGER REFERENCES orders ON DELETE SET NULL,
        message VARCHAR (50) NOT NULL,
        is_seen BOOL DEFAULT FALSE,
        created_on TIMESTAMP DEFAULT NOW()
        );"""

    create_admin ="""INSERT INTO users (username, password, email, is_admin)
                VALUES ('admin', 'password', 'jratcher@gmail.com', True);"""
    
    create_user ="""INSERT INTO users (username, password, email, is_admin)
                VALUES ('dan', 'password', 'dan@gmail.com', False);"""

    return [user_table, order_table, notifications, create_admin, create_user]

if __name__ == '__main__':
    print(DbConnect('test').delete_latest_user())