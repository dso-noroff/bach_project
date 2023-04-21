from helper_dataset import DatasetHelper
from helper_distance import DistanceHelper


def calculate_emission(avg_emission_tkm, distance_km, weight_kg):
    """
    Calculate the emission for a product
    :param avg_emission_tkm: Average emission for a ton pr km
    :param distance_km: Distance in km
    :param weight_kg: Weight in kg
    :return: Emission in kg
    """
    emission_pr_km_kg = avg_emission_tkm / 1000
    return round((emission_pr_km_kg * weight_kg) * distance_km / 1000, 2)


def print_values(product,
                 category,
                 warehouse1,
                 warehouse2,
                 warehouse_transport_options,
                 transportations):
    distance = DistanceHelper.calculate_distance_between_coordinates(warehouse1['latitude'].values[0],
                                                                     warehouse1['longitude'].values[0],
                                                                     warehouse2['latitude'].values[0],
                                                                     warehouse2['longitude'].values[0])
    print("")
    print("###" * 50)
    print(f"Product: {product['name'].values[0]} with weight {product['weight'].values[0]} kg")
    print(
        f"Production emission cost for {product['name'].values[0]} is "
        f"{category['co2emission'].values[0]} CO2 pr {category['unit'].values[0]}")

    print("")
    print(f"Transportation from {warehouse1['name'].values[0]} to {warehouse2['name'].values[0]}")
    print(f"\tDistance between {warehouse1['name'].values[0]} and {warehouse2['name'].values[0]} is {distance} km")
    print("\tTransportation CO2 emissions:")
    for index, row in warehouse_transport_options.iterrows():
        transport = transportations[transportations['id'] == row['transportation_id']]
        print(
            f"\t\t{transport['transport'].values[0]} "
            f"- {transport['fuel'].values[0]}: "
            f"{calculate_emission(transport['avg_emission_tkm'].values[0], distance, product['weight'].values[0])} kg")
        print(
            f"\t\t\tAverage CO2 emission for {transport['transport'].values[0]} - "
            f"{transport['fuel'].values[0]} is {transport['avg_emission_tkm'].values[0]} kg pr ton pr km")
    print("###" * 50)
    print("")


if __name__ == '__main__':
    dsHelp = DatasetHelper()

    list_warehouses = dsHelp.load_warehouses()
    list_transportations = dsHelp.load_transportations()
    warehouse_transportation_options = dsHelp.load_warehouse_transport_options()

    warehouse_1 = list_warehouses.sample(1)
    warehouse_2 = list_warehouses.sample(1)

    warehouse1_transport_options = warehouse_transportation_options[
        warehouse_transportation_options['warehouse_id'] == warehouse_1['id'].values[0]]
    warehouse2_transport_options = warehouse_transportation_options[
        warehouse_transportation_options['warehouse_id'] == warehouse_2['id'].values[0]]

    list_products = dsHelp.load_products()
    list_categories = dsHelp.load_categories()

    for i in range(0, 2):
        p1 = list_products.sample(1)
        c1 = list_categories[list_categories['id'] == p1['category_id'].values[0]]
        d = DistanceHelper.calculate_distance_between_coordinates(warehouse_1['latitude'].values[0],
                                                                  warehouse_1['longitude'].values[0],
                                                                  warehouse_2['latitude'].values[0],
                                                                  warehouse_2['longitude'].values[0])
        print_values(p1, c1, warehouse_1, warehouse_2, warehouse1_transport_options, list_transportations)
