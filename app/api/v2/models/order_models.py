from app.api.utils.validators import Validator
from .user_models import DataBase
from app.db_config import drop_tables, create_tables



class Orders(DataBase):
    """Handles order tables operations"""
    def add_order(self, order_list):
        is_succesful = False
        is_valid = self.validators.order_list_validator(order_list)
        order_dict = {'user_id': order_list[0], 'recepient_name': order_list[1], 'recepient_no': order_list[2], 'weight': order_list[3], 'pickup': order_list[4], 'dest': order_list[5]}
        query = """INSERT INTO orders (user_id,recepient_name, recepient_no, weight, pickup, current_location, dest)
                VALUES ({user_id}, '{recepient_name}', '{recepient_no}',{weight}, '{pickup}', '{pickup}', '{dest}');""".format(**order_dict)
        if is_valid:
            self.cursor.execute(query)
            self.conn.commit()
            is_succesful = True
        return is_succesful  
    
    def get_order(self, order_id):
        query = """SELECT  user_id,recepient_name, recepient_no, weight, pickup, dest, status FROM users WHERE order_id = {};""".format(order_id)
        self.cursor.execute(query)
        order = self.cursor.fetchone()
        order_dict = {order_id: [order[0], order[1], order[2], order[3], order[4], order[5], order[6]]}
        return order_dict

    def get_all_orders(self):
        """Gets all orders"""
        query = """SELECT order_id, user_id, pickup, dest, current_location, weight, status FROM orders;"""
        self.cursor.execute(query)
        orders = self.cursor.fetchall()
        orders_dict = {}
        if orders:
            for order in orders:
                orders_dict[order[0]] = [order[1], order[2], order[3]]
        return orders_dict


    def get_users_orders(self, user_id):
        """Gets all users' orders"""
        query = """SELECT order_id, user_id, pickup, dest, current_location, weight, status FROM orders where user_id = {};""".format(user_id)
        self.cursor.execute(query)
        orders = self.cursor.fetchall()
        orders_dict = {}
        if orders:
            for order in orders:
                orders_dict[order[0]] = [order[1], order[2], order[3]]
        return False

    def is_order_there(self, order_id):
        """Check if order is there"""
        is_there = True
        query = """SELECT  user_id FROM order WHERE order_id = {};""".format(order_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if not result:
            is_there = False
        return is_there



    def cancel_order(self, order_id, user_id):
        """Updates status column to cancelled"""
        query = """UPDATE SET status='Canceled' where order_id = {};""".format(order_id)
        query1 = """INSERT INTO notification (user_id, order_id, message) VALUES ({}, {}, 'Order canceled');""".format(user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()
        

    def deliver_order(self, user_id, order_id):
        """Updates status column to delivered"""
        query = """UPDATE SET status='Delivered' where order_id = {};""".format(order_id)
        query1 = """INSERT INTO notification (user_id, order_id, message) VALUES ({}, {}, 'Parcel delivered');""".format(user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def change_current_loc(self, user_id, order_id, curr_loc,):
        """Updates current parcel location"""
        query = """UPDATE SET current_location='{}' where order_id = {};""".format(curr_loc, order_id)
        query1 = """INSERT INTO notification (user_id, order_id, message) VALUES ({}, {}, 'Current location updated');""".format(user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def change_dest_loc(self, user_id, order_id, dest_loc):
        """Updates parcel destination location"""
        query = """UPDATE SET current_location='{}' where order_id = {};""".format(dest_loc, order_id)
        query1 = """INSERT INTO notification (user_id, order_id, message) VALUES ({}, {}, 'Current location updated');""".format(user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()




   # Orders().add_order({'user_id': 23, 'recepient_name': ''  })
