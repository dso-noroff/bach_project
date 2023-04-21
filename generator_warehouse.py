import pandas as pd
import random

from helper_dataset import DatasetHelper


class WarehouseProductAvailabilityGenerator:
    def __init__(self, products, warehouses):
        self.products = products
        self.warehouses = warehouses

    def generate(self):
        warehouse_count = len(self.warehouses)
        product_count = len(self.products)

        res = pd.DataFrame(columns=['warehouse_id', 'product_id', 'quantity'])

        for i in range(warehouse_count):
            for j in range(product_count):

                # Check if warehouse and product are already in the result
                if len(res[(res['warehouse_id'] == self.warehouses[i][0]) & (
                        res['product_id'] == self.products[j][0])]) == 0:
                    res.loc[len(res)] = [self.warehouses[i][0], self.products[j][0], generate_random_quantity()]

        # Sort by warehouse_id and product_id
        res = res.sort_values(by=['warehouse_id', 'product_id'])
        return res

    def generate_random_product_availability(self):
        warehouse = random.choice(self.warehouses)
        product = random.choice(self.products)
        quantity = generate_random_quantity()
        return [warehouse[0], product[0], quantity]


def generate_random_quantity():
    return random.randint(0, 10)


# Path: main.py
if __name__ == '__main__':
    ds_helper = DatasetHelper()

    list_products = ds_helper.load_products()
    list_warehouses = ds_helper.load_warehouses()

    warehouse_availability_generator = WarehouseProductAvailabilityGenerator(list_products, list_warehouses)
    warehouse_availability = warehouse_availability_generator.generate()

    ds_helper.write_warehouse_product_availability(warehouse_availability)

    print(len(warehouse_availability_generator.products))
    print(len(warehouse_availability_generator.warehouses))
