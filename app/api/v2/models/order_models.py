
from app.api.v2.utils.validators import Validator
from .user_models import DataBase

message = 'message'


class Orders(DataBase):
    """Handles order tables operations""" 

    def add_order(self, order, user_id):
        """Saves order to database"""
        messo = self.validators.order_list_validator(order)
        if not messo == True:
            return messo

        order['user_id'] = user_id

        query = """INSERT INTO orders (user_id, recepient_name, recepient_no, weight, pickup, current_location, dest)
                VALUES ({user_id}, '{recepient_name}', '{recepient_no}',{weight}, '{pickup}', '{pickup}', '{dest}') RETURNING order_id;""".format(**order)

        self.cursor.execute(query)
        order_id = self.cursor.fetchone()[0]
        self.conn.commit()
        order['order_id'] = order_id
        return order

    def get_order(self, order_id):
        query = """SELECT order_id, user_id, pickup, dest, current_location, weight, status, recepient_no, recepient_name  FROM orders WHERE order_id = {};""".format(
            order_id)
        self.cursor.execute(query)
        order = self.cursor.fetchone()
        if order:
            order_dict = {
                'order_id': order[0],
                'user_id': order[1],
                'pickup': order[2],
                'dest': order[3],
                'curr_loc': order[4],
                'weight': order[5],
                'status': order[6],
                'recepient_no': order[7],
                'recepient_name': order[8]

            }
            return order_dict
        return False

    def get_all_orders(self):
        """Gets all orders"""
        query = """SELECT order_id, user_id, pickup, dest, current_location, weight, status FROM orders;"""
        self.cursor.execute(query)
        orders = self.cursor.fetchall()
        orders_list = []
        if orders:
            for order in orders:
                orders_list.append({
                    'order_id': order[0],
                    'user_id': order[1],
                    'pickup': order[2],
                    'dest': order[3],
                    'curr_loc': order[4],
                    'weight': order[5],
                    'status': order[6],
                })
        return orders_list

    def get_users_orders(self, user_id):
        """Gets all users' orders"""
        query = """SELECT order_id, user_id, pickup, dest, current_location, weight, status FROM orders where user_id = {};""".format(
            user_id)
        self.cursor.execute(query)
        orders = self.cursor.fetchall()
        orders_list = []
        if orders:
            for order in orders:
                order_dict = {
                    'order_id': order[0],
                    'user_id': order[1],
                    'pickup': order[2],
                    'dest': order[3],
                    'curr_loc': order[4],
                    'weight': order[5],
                    'status': order[6]
                }
                orders_list.append(order_dict)
            return orders_list
        return False

    def cancel_order(self, order_id, user_id):
        """Updates status column to cancelled"""
        query = """UPDATE orders SET status = 'Canceled' WHERE order_id = {};""".format(
            order_id)
        query1 = """INSERT INTO notifications (user_id, order_id, message) VALUES ({}, {}, 'Order canceled');""".format(
            user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def deliver_order(self, user_id, order_id):
        """Updates status column to delivered"""
        query = """UPDATE orders SET status = 'Delivered' WHERE order_id = {};""".format(
            order_id)
        query1 = """INSERT INTO notifications (user_id, order_id, message) VALUES ({}, {}, 'Parcel delivered');""".format(
            user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def change_current_loc(self, user_id, order_id, curr_loc,):
        """Updates current parcel location"""
        query = """UPDATE orders SET current_location = '{}' where order_id = {};""".format(
            curr_loc, order_id)
        query1 = """INSERT INTO notifications (user_id, order_id, message) VALUES ({}, {}, 'Current location updated');""".format(
            user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def change_dest_loc(self, user_id, order_id, dest_loc):
        """Updates parcel destination location"""
        query = """UPDATE orders SET current_location='{}' where order_id = {};""".format(
            dest_loc, order_id)
        query1 = """INSERT INTO notifications (user_id, order_id, message) VALUES ({}, {}, 'Current location updated');""".format(
            user_id, order_id)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def get_order_status(self, order_id):
        """Gets the order status"""
        query = """SELECT status FROM orders WHERE order_id = {};""".format(
            order_id)
        self.cursor.execute(query)
        status = self.cursor.fetchone()
        if status:
            status = status[0]
        return status

   # Orders().add_order({'user_id': 23, 'recepient_name': ''  })
