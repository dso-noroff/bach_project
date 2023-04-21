from helper_distance import DistanceHelper


class TransportationHelper:

    @staticmethod
    def calculate_categorized_transportation_cost(transportation_method, dist):
        """
        # Calculate categorized transportation score
        :param transportation_method: Transportation method
        :param dist: Distance
        :return: Transportation cost
        """
        transportation_co2_emission = transportation_method['avg_emission_kg_km']
        total_transportation_cost = dist * transportation_co2_emission

        # Categorize
        if total_transportation_cost <= transportation_method['25th_percentile']:
            return total_transportation_cost, 'Very low'
        elif total_transportation_cost <= transportation_method['50th_percentile']:
            return total_transportation_cost, 'Low'
        elif total_transportation_cost <= transportation_method['75th_percentile']:
            return total_transportation_cost, 'Medium'
        else:
            return total_transportation_cost, 'High'

    @staticmethod
    def calculate_transportation_cost_for_location(transportation_df,
                                                   lat_1,
                                                   long1,
                                                   lat2,
                                                   long2):
        """
        Calculate transportation cost between two locations
        :param transportation_df: Transportation dataframe
        :param lat_1: Latitude 1
        :param long1: Longitude 1
        :param lat2: Latitude 2
        :param long2: Longitude 2
        :return: Transportation cost
        """
        drive_dist = DistanceHelper.driving_distance_between_coordinates(lat_1,
                                                                         long1,
                                                                         lat2,
                                                                         long2) / 1000

        tran_cost = []
        for j in range(len(transportation_df)):
            trans = transportation_df.iloc[j]
            trans_name = trans['transport']

            tran_cost.append((trans_name,
                              TransportationHelper.calculate_categorized_transportation_cost(trans, drive_dist)))

        return tran_cost

    @staticmethod
    def calculate_transportation_for_closest(df_warehouse, df_transportation, warehouses, user):
        """
        Calculate transportation cost for 5 closest warehouses
        :param df_warehouse: Warehouse dataframe
        :param df_transportation: Transportation dataframe
        :param warehouses: Warehouses
        :param user: User
        :return: Transportation cost
        """
        warehouse_transportation_cost = {}
        for w in range(len(warehouses)):
            warehouse_id = list(warehouses.keys())[w]
            warehouse = df_warehouse[df_warehouse['id'] == warehouse_id]

            warehouse_lat = warehouse['latitude'].values[0]
            warehouse_long = warehouse['longitude'].values[0]

            warehouse_transportation_cost[warehouse_id] = TransportationHelper \
                .calculate_transportation_cost_for_location(df_transportation,
                                                            user['latitude'],
                                                            user['longitude'],
                                                            warehouse_lat,
                                                            warehouse_long)

        # Sort by environment friendly from lowest to highest
        warehouse_transportation_cost = {k: v for k, v in
                                         sorted(warehouse_transportation_cost.items(), key=lambda item: item[1][0][0])}

        return warehouse_transportation_cost
