import json
from math import sin, cos, sqrt, atan2, radians
import googlemaps


class DistanceHelper:

    @staticmethod
    def driving_distance_between_coordinates(lat1, long1, lat2, long2):
        """
        Calculate the driving distance between two coordinates
        :param lat1: Latitude of the first coordinate
        :param long1: Longitude of the first coordinate
        :param lat2: Latitude of the second coordinate
        :param long2: Longitude of the second coordinate
        :return: Distance in meters
        """
        api_key = '___ENTER_API_KEY____'
        g_maps = googlemaps.Client(key=api_key)

        origin = (lat1, long1)
        destination = (lat2, long2)

        result = g_maps.distance_matrix(origin, destination, mode='driving')
        distance = result['rows'][0]['elements'][0]['distance']['value']
        return distance

    @staticmethod
    def calculate_distance_between_coordinates(latitude1, longitude1, latitude2, longitude2):
        """
        Calculate the distance between two coordinates
        :param latitude1: Latitude of the first coordinate
        :param longitude1: Longitude of the first coordinate
        :param latitude2: Latitude of the second coordinate
        :param longitude2: Longitude of the second coordinate
        :return: Distance using airline in meters
        """
        radius = 6373.0

        lat1 = radians(latitude1)
        lon1 = radians(longitude1)
        lat2 = radians(latitude2)
        lon2 = radians(longitude2)

        distance_lon = lon2 - lon1
        distance_lat = lat2 - lat1

        a = sin(distance_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(distance_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = radius * c

        return round(distance, 2)
