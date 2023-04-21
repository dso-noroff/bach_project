from generator_order import OrderGenerator, Order
from helper_dataset import DatasetHelper
from helper_numerical import HelperNumerical
from faker import Faker
import random


class UserOrderGenerator:

    def __init__(self,
                 users,
                 products,
                 warehouses,
                 transportations,
                 products_available_in_warehouse,
                 transportations_available_for_warehouse):
        self.users = users
        self.products = products
        self.warehouses = warehouses
        self.transportations = transportations
        self.products_available_in_warehouse = products_available_in_warehouse
        self.transportations_available_for_warehouse = transportations_available_for_warehouse

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
    def get_transportation_for_warehouse(self, warehouse, transportations_available_for_warehouse):
        warehouse_id = warehouse["id"].values[0]

        transportation_found = False
        transportation = None

        while not transportation_found:
            transportation = UserOrderGenerator.get_random_value_from_dataframe(self.transportations)
            transportation_id = transportation["id"].values[0]

            transportation_available = transportations_available_for_warehouse[
                (transportations_available_for_warehouse["warehouse_id"] == warehouse_id) &
                (transportations_available_for_warehouse["transportation_id"] == transportation_id)
                ]

            if len(transportation_available) > 0:
                transportation_found = True

        return transportation

    @staticmethod
    def generate_user_order(self,
                            users,
                            products,
                            products_available_in_warehouse,
                            transportations_available_for_warehouse):
        fake = Faker()

        o_id = 1

        # How many users and products to use for testing purposes
        use_users = len(users)
        use_products = len(products)

        for i in range(1, use_users + 1):
            user = users.loc[users["id"] == i]
            user_id = user["id"].values[0]

            print("Generating orders for user: " + str(user_id))

            for j in range(1, use_products + 1):

                print("Generating order for product: " + str(j))

                order_id = o_id
                order_quantity = HelperNumerical.get_weighted_random(0, 4)

                date_start = fake.date_time_between(start_date='-2y', end_date='now')
                date_end = fake.date_time_between(start_date=date_start, end_date='now')
                order_date = fake.date_time_between(start_date=date_start, end_date=date_end)

                warehouse = UserOrderGenerator.get_warehouse_near_coordinates(self, user)
                warehouse_id = warehouse["id"].values[0]

                product = products.loc[products["id"] == j]
                product_id = product["id"].values[0]

                # Check if the product is available in the warehouse
                product_available = products_available_in_warehouse[
                    (products_available_in_warehouse["warehouse_id"] == warehouse_id) &
                    (products_available_in_warehouse["product_id"] == product_id)
                    ]

                price_pr_unit = products[products["id"] == product_id]["price_pr_unit"].values[0]
                transportation = UserOrderGenerator \
                    .get_transportation_for_warehouse(self,
                                                      warehouse,
                                                      transportations_available_for_warehouse)

                transportation_id = transportation["id"].values[0]

                if len(product_available) == 0:
                    order_quantity = 0
                    price_pr_unit = 0
                    transportation_id = 0

                order = Order(order_id,
                              user_id,
                              warehouse_id,
                              product_id,
                              transportation_id,
                              order_quantity,
                              price_pr_unit,
                              order_date)

                print("Saving order: " + str(order_id))

                ds.append_user_order(order)

                o_id += 1


if __name__ == '__main__':
    ds = DatasetHelper()

    u = ds.load_users()
    p = ds.load_products()
    w = ds.load_warehouses()
    t = ds.load_transportations()
    p_a = ds.load_warehouse_product_availability()
    t_a_w = ds.load_warehouse_transport_options()

    ds.clear_user_orders()

    o = UserOrderGenerator(users=u,
                           products=p,
                           warehouses=w,
                           transportations=t,
                           products_available_in_warehouse=p_a,
                           transportations_available_for_warehouse=t_a_w
                           )

    o.generate_user_order(o,
                          users=u,
                          products=p,
                          products_available_in_warehouse=p_a,
                          transportations_available_for_warehouse=t_a_w)
