import pandas as pd
import codecs


class DatasetHelper:
    def __init__(self):
        pass

    # LOADERS
    @staticmethod
    def load_categories():
        categories = pd.read_csv('./data/categories.csv', delimiter=',')
        return categories

    @staticmethod
    def load_products():
        products = pd.read_csv('./data/products.csv', delimiter=',')
        return products

    @staticmethod
    def load_orders():
        orders = pd.read_csv('./data/orders.csv', delimiter=',')
        return orders

    @staticmethod
    def load_orders_100k():
        orders = pd.read_csv('./data/orders_100k.csv', delimiter=',')
        return orders

    @staticmethod
    def load_orders_1m():
        orders = pd.read_csv('./data/orders_1m.csv', delimiter=',')
        return orders

    @staticmethod
    def load_users():
        users = pd.read_csv('./data/users.csv', delimiter=',')
        return users

    @staticmethod
    def load_users_10k():
        users = pd.read_csv('./data/users_10k.csv', delimiter=',')
        return users

    @staticmethod
    def load_users_100k():
        users = pd.read_csv('./data/users_100k.csv', delimiter=',')
        return users

    @staticmethod
    def load_transportations():
        transportations = pd.read_csv('./data/transportations.csv', delimiter=',')
        return transportations

    @staticmethod
    def load_warehouses():
        warehouses = pd.read_csv('./data/warehouses.csv', delimiter=',')
        return warehouses

    @staticmethod
    def load_warehouse_product_availability():
        warehouse_product_availability = pd.read_csv('./data/warehouse_product_availability.csv', delimiter=',')
        return warehouse_product_availability

    @staticmethod
    def load_warehouse_transport_options():
        warehouse_transport_options = pd.read_csv('./data/warehouse_transportation_options.csv', delimiter=',')
        return warehouse_transport_options

    # WRITERS
    @staticmethod
    def write_orders(orders):
        with open('./data/orders.csv', 'w') as f:
            f.write(orders.to_csv(index=False, line_terminator='\n'))

    @staticmethod
    def write_warehouse_product_availability(warehouse_product_availability):
        with open('./data/warehouse_product_availability.csv', 'w') as f:
            f.write(warehouse_product_availability.to_csv(index=False, line_terminator='\n'))

    @staticmethod
    def write_users(users):
        with open('./data/users.csv', 'w') as f:
            f.write(users.to_csv(index=False, line_terminator='\n'))

    @staticmethod
    def write_products(products):
        with codecs.open('./data/products.csv', 'w', encoding='utf-8') as f:
            f.write(products.to_csv(index=False, line_terminator='\n'))

    # APPENDERS
    @staticmethod
    def append_order(order):
        with open('./data/orders.csv', 'a+') as f:
            f.write(f"{order.order_id},{order.order_date.date()},{order.order_date.timestamp()},{order.user_id},"
                    f"{order.warehouse_id},{order.transportation_id},{order.product_id},{order.price_pr_unit},"
                    f"{order.order_quantity} \n")

    # CLEARER'S
    @staticmethod
    def clear_orders():
        with open('./data/orders.csv', 'w') as f:
            f.write('')
