import psycopg2
from flask import current_app as app


POSTGRES = {
    'user': 'elmonstro',
    'pw': "password",
    'db': 'sendit',
    'host': 'localhost',
    'port': '5432',
}

url = 'postgresql://{user}:{pw}@{host}:{port}/{db}' .format(**POSTGRES)

def get_connection(url):
    """Creates and return connection"""
    conn = psycopg2.connect(url)
    return conn

def init_dbase(url):
    """Start database"""
    psycopg2.connect(url)

    

def create_tables(url):
    """Create tabes"""
    queries = create_queries()
    conn = get_connection(url)
    cursor = conn.cursor()
    db_name = url.split('/')[-1]
    if db_name == 'test_db':
        queries.pop()

    try:
        for query in queries:
            cursor.execute(query)
    except psycopg2.IntegrityError:
        pass
    conn.commit()

def drop_tables():
    """Delete tables"""
    query = """DROP TABLE IF EXISTS users, orders, notifications CASCADE; """
    conn = get_connection(url)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

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
        order_id INTEGER REFERENCES orders,
        message VARCHAR (50) NOT NULL,
        is_seen BOOL DEFAULT FALSE,
        created_on TIMESTAMP DEFAULT NOW()
        );"""

    create_admin ="""INSERT INTO users (username, password, email, is_admin)
                VALUES ('admin', 'password', 'jratcher@gmail.com', True);"""
    
    create_user ="""INSERT INTO users (username, password, email, is_admin)
                VALUES ('dan', 'password', 'dan@gmail.com', False);"""

    return [user_table, order_table, notifications, create_admin, create_user]
