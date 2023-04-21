import pandas as pd
import random
import faker as fake

from helper_dataset import DatasetHelper


def create_users(warehouses):
    users = pd.DataFrame(columns=['id', 'name', 'latitude', 'longitude'])
    for i in range(1, 1001):
        # Create a random name
        name = fake.Faker().name()

        # Get random warehouse
        warehouse = warehouses.sample(1)

        # Add some random noise to the warehouse coordinates
        latitude = warehouse["latitude"].values[0] + random.uniform(-0.04999, 0.04999)
        longitude = warehouse["longitude"].values[0] + random.uniform(-0.09999, 0.09999)

        # Add user to the DataFrame
        users.loc[len(users)] = [i, name, latitude, longitude]

    return users


if __name__ == '__main__':
    ds_helper = DatasetHelper()
    list_warehouses = ds_helper.load_warehouses()
    list_new_users = create_users(list_warehouses)
    ds_helper.write_users(list_new_users)
