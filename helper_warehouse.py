import itertools
from helper_distance import DistanceHelper


class WarehouseHelper:

    @staticmethod
    def get_warehouse_with_product_in_stock(df, product_id):
        """
        Get warehouses with product in stock
        :param df: Dataframe
        :param product_id: Product ID
        :return: Warehouses with product in stock
        """
        warehouses_with_product_stock = df[df['product_id'] == product_id]
        # Remove warehouses with no stock
        warehouses_with_product_stock = warehouses_with_product_stock[warehouses_with_product_stock['quantity'] > 0]

        return warehouses_with_product_stock

    @staticmethod
    def get_closest_warehouse(df_warehouse, df_warehouse_availability, user, product_id):
        """
        Get the closest warehouse
        :param df_warehouse: Warehouses dataframe
        :param df_warehouse_availability: Warehouse availability dataframe
        :param user: User
        :param product_id: Product ID
        :return: Closest warehouse
        """
        user_lat = user['latitude']
        user_long = user['longitude']

        # Get warehouses with product
        warehouses_with_product_stock = WarehouseHelper.get_warehouse_with_product_in_stock(df_warehouse_availability,
                                                                                            product_id)
        warehouse_dict = {}

        # Get the closest warehouse
        for w in range(len(warehouses_with_product_stock)):
            warehouse_stock = warehouses_with_product_stock.iloc[w]

            warehouse_id = warehouse_stock['warehouse_id']

            warehouse = df_warehouse[df_warehouse['id'] == warehouse_id]

            warehouse_lat = warehouse['latitude'].values[0]
            warehouse_long = warehouse['longitude'].values[0]

            # Calculate distance
            dist = DistanceHelper.driving_distance_between_coordinates(user_lat,
                                                                       user_long,
                                                                       warehouse_lat,
                                                                       warehouse_long) / 1000

            warehouse_dict[warehouse_id] = dist

        # Sort by distance
        warehouse_dict = {k: v for k, v in sorted(warehouse_dict.items(), key=lambda item: item[1])}

        return warehouse_dict

    @staticmethod
    def get_5_closest_warehouses(df_warehouse, df_warehouse_availability, user, product_id):
        """
        Get 5 closest warehouses
        :param df_warehouse: Warehouse dataframe
        :param df_warehouse_availability: Warehouse availability dataframe
        :param user: User
        :param product_id: Product ID
        :return: 5 closest warehouses
        """
        closest_w = WarehouseHelper.get_closest_warehouse(df_warehouse, df_warehouse_availability, user, product_id)

        # Sort by distance
        closest_w = {k: v for k, v in sorted(closest_w.items(), key=lambda item: item[1])}

        # Get 5 closest warehouses
        closest_w = dict(itertools.islice(closest_w.items(), 5))

        return closest_w
