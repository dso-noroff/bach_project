import random
import pandas as pd
from faker import Faker

from helper_dataset import DatasetHelper
from helper_numerical import HelperNumerical
from models.Order import Order


class OrderGenerator:
    def __init__(self,
                 warehouses,
                 products,
                 users,
                 transportations,
                 warehouse_product_availability,
                 transportations_available_for_warehouse):
        self.warehouses = warehouses
        self.products = products
        self.users = users
        self.transportations = transportations
        self.warehouse_product_availability = warehouse_product_availability
        self.transportations_available_for_warehouse = transportations_available_for_warehouse

    @staticmethod
    def get_random_value_from_dataframe(df):
        rnd_value = random.randint(1, len(df))

        rnd_modifier = random.randint(1, 10)
        if rnd_modifier % 2 == 0:
            rnd_value2 = rnd_value + 1
            if rnd_value2 > len(df):
                rnd_value2 = rnd_value - 1
            return df[df["id"] == rnd_value2]
        else:
            rnd_value3 = rnd_value - 1
            if rnd_value3 < 1:
                rnd_value3 = rnd_value + 1

        return df[df["id"] == rnd_value3]

    @staticmethod
    def get_warehouse_near_coordinates(self, user):
        user_lat = user["latitude"].values[0]
        user_long = user["longitude"].values[0]

        warehouse_found = False
        warehouse = None
        total_warehouses = len(self.warehouses)
        counter = 0
        while not warehouse_found:
            warehouse = OrderGenerator.get_random_value_from_dataframe(self.warehouses)
            warehouse_lat = warehouse["latitude"].values[0]
            warehouse_long = warehouse["longitude"].values[0]

            if abs(user_lat - warehouse_lat) <= 0.5 and abs(user_long - warehouse_long) <= 0.5:
                warehouse_found = True

            counter += 1

            if counter > total_warehouses:
                break

        return warehouse

    @staticmethod
    def get_product_available_in_warehouse(self, warehouse, warehouse_product_availability):
        warehouse_id = warehouse["id"].values[0]

        product_found = False
        product = None

        while not product_found:
            product = OrderGenerator.get_random_value_from_dataframe(self.products)
            product_id = product["id"].values[0]

            product_available = warehouse_product_availability[
                (warehouse_product_availability["warehouse_id"] == warehouse_id) &
                (warehouse_product_availability["product_id"] == product_id)
                ]

            if len(product_available) > 0:
                product_found = True

        return product

    @staticmethod
    def get_transportation_for_warehouse(self, warehouse, transportations_available_for_warehouse):
        warehouse_id = warehouse["id"].values[0]

        transportation_found = False
        transportation = None

        while not transportation_found:
            transportation = OrderGenerator.get_random_value_from_dataframe(self.transportations)
            transportation_id = transportation["id"].values[0]

            transportation_available = transportations_available_for_warehouse[
                (transportations_available_for_warehouse["warehouse_id"] == warehouse_id) &
                (transportations_available_for_warehouse["transportation_id"] == transportation_id)
                ]

            if len(transportation_available) > 0:
                transportation_found = True

        return transportation

    def generate_orders(self, order_id):
        fake = Faker()
        user = OrderGenerator.get_random_value_from_dataframe(self.users)
        warehouse = OrderGenerator.get_warehouse_near_coordinates(self, user)
        product = OrderGenerator.get_product_available_in_warehouse(self,
                                                                    warehouse,
                                                                    self.warehouse_product_availability)
        transportation = OrderGenerator.get_transportation_for_warehouse(self,
                                                                         warehouse,
                                                                         self.transportations_available_for_warehouse)

        warehouse_id = warehouse["id"].values[0]
        product_id = product["id"].values[0]
        user_id = user["id"].values[0]
        transportation_id = transportation["id"].values[0]

        price_pr_unit = self.products[self.products["id"] == product_id]["price_pr_unit"].values[0]
        order_quantity = HelperNumerical.get_weighted_random(0, 4)

        date_start = fake.date_time_between(start_date='-2y', end_date='now')
        date_end = fake.date_time_between(start_date=date_start, end_date='now')

        order_date = fake.date_time_between(start_date=date_start, end_date=date_end)

        return Order(order_id,
                     user_id,
                     warehouse_id,
                     product_id,
                     price_pr_unit,
                     order_quantity,
                     transportation_id,
                     order_date)


if __name__ == '__main__':
    ds_helper = DatasetHelper()
    list_warehouse = ds_helper.load_warehouses()
    list_warehouse_product_availability = ds_helper.load_warehouse_product_availability()
    list_products = ds_helper.load_products()
    list_users = ds_helper.load_users()
    list_transportations = ds_helper.load_transportations()
    list_warehouse_transportations = ds_helper.load_warehouse_transport_options()
    order_generator = OrderGenerator(list_warehouse,
                                     list_products,
                                     list_users,
                                     list_transportations,
                                     list_warehouse_product_availability,
                                     list_warehouse_transportations)

    ds_helper.clear_orders()

    orders = pd.DataFrame(
        columns=['order_id',
                 'order_date',
                 'order_time_stamp',
                 'user_id',
                 'warehouse_id',
                 'transportation_id',
                 'product_id',
                 'price_pr_unit',
                 'order_quantity'])
    for i in range(1, 100001):
        order = order_generator.generate_orders(i)
        ds_helper.append_order(order)
