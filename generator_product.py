import random

import pandas as pd

from helper_dataset import DatasetHelper
from models.Product import Product


def enrich_products(product_list):
    products = pd.DataFrame(columns=[
        'id',
        'name',
        'category_id',
        'price_pr_unit',
        'co2',
        'co2per_kg',
        'weight',
        'color'
    ])

    for i in range(len(product_list)):
        p = product_list.iloc[i]
        product_id = p['id']
        name = p['name']
        category_id = p['category_id']
        price_pr_unit = p['price_pr_unit']
        co2 = p['co2']
        co2per_kg = p['co2per_kg']
        weight = p['weight']
        color = random.choice(
            ["red",
             "green",
             "blue",
             "yellow",
             "black",
             "white",
             "grey",
             "brown",
             "pink",
             "purple"
             ])

        p = Product(product_id,
                    name,
                    category_id,
                    price_pr_unit,
                    co2,
                    co2per_kg,
                    color,
                    weight)

        products = products.append(
            {'id': p.product_id,
             'name': p.name,
             'category_id': p.category_id,
             'price_pr_unit': p.price_pr_unit,
             'co2': p.co2,
             'co2per_kg': p.co2_per_kg,
             'weight': p.weight,
             'color': p.color, },
            ignore_index=True)

    return products


if __name__ == '__main__':
    product = DatasetHelper().load_products()
    product = enrich_products(product)
    DatasetHelper().write_products(product)
