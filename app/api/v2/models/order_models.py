
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

    def change_order_status(self, order_id=None, status=None):
        """Updates status column to delivered"""
        user_id = self.get_order(order_id)['user_id']
        if status == "Rejected":
            notification_message = "Parcel delivery order {} rejected"
        elif status == "In-transit": 
            notification_message = "Parcel delivery order {} accepted"
        elif status == "Delivered":
            notification_message = "Parcel delivery order {} delivered"
        elif status == "Canceled":
            notification_message = "Parcel delivery order {} canceled"
            user_id = 1
        notification_message.format(order_id)

        query = """UPDATE orders SET status = '{}' WHERE order_id = {};""".format(status,
                                                                                  order_id)
        
        query1 = """INSERT INTO notifications (user_id, order_id, message) VALUES ({}, {}, '{}');""".format(
            user_id, order_id, notification_message)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()

    def change_location(self, order_id=None, column=None, location=None):
        """Changes order locations"""
        user_id = self.get_order(order_id)['user_id']
        if column == "current_location":
            notification_message = "Current location of parcel {} has been changed to {}".format(order_id,
                location)
        elif column == "dest":
            notification_message = "Destination location of parcel {} has been changed to {}".format(order_id,
                location)
            user_id = 1
            
        """Updates current parcel location"""
        query = """UPDATE orders SET {} = '{}' where order_id = {};""".format(column,
                                                                              location, order_id)
        query1 = """INSERT INTO notifications (user_id, order_id, message) VALUES ({}, {}, '{}');""".format(
            user_id, order_id, notification_message)
        self.cursor.execute(query)
        self.cursor.execute(query1)
        self.conn.commit()
