import plotly.express as px
import matplotlib.pyplot as plt
import openrouteservice as ors
import folium
from openrouteservice import convert

from helper_distance import DistanceHelper


class GraphsHelper:

    @staticmethod
    def plot_distribution(df, column, title, x_label=None, y_label=None):
        """
        Plot distribution of a column
        :param df: Dataframe
        :param column: Column name
        :param title: Title of the plot
        :param x_label: X axis label
        :param y_label: Y axis label
        :return: None
        """
        category_distribution = df[column].value_counts()
        category_distribution = category_distribution.reset_index()
        category_distribution.columns = [column, 'count']

        fig = px.bar(category_distribution, x=column, y='count', title=title)
        fig.update_xaxes(title_text=x_label)
        fig.update_yaxes(title_text=y_label)
        fig.show()

    @staticmethod
    def plot_coordinates(df, title):
        """
        Plot coordinates on a map
        :param df: Dataframe
        :param title: Title of the plot
        :return: None
        """
        plt.figure(figsize=(10, 10))
        plt.scatter(df['longitude'], df['latitude'], s=20, c='red')

        plt.title(title)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

    @staticmethod
    def get_min_max_coordinate(df, column_name):
        """
        Get min and max coordinates
        :param df: Dataframe
        :param column_name: Column name
        :return: Min and max coordinates
        """
        min_latitude = df[column_name].min()
        max_latitude = df[column_name].max()
        return min_latitude, max_latitude

    @staticmethod
    def plot_driving_distance(from_lat, from_long, from_name, to_lat, to_long, to_name):
        """
        Plot driving distance between two coordinates
        :param from_lat: From latitude
        :param from_long: From longitude
        :param from_name: From name
        :param to_lat: From latitude
        :param to_long: From longitude
        :param to_name: From name
        :return: None
        """

        driving_distance = DistanceHelper.driving_distance_between_coordinates(from_lat,
                                                                               from_long,
                                                                               to_lat,
                                                                               to_long) / 1000

        client = ors.Client(key='___ENTER_API_KEY____')
        # Set location coordinates in longitude,latitude order
        coords = ((from_long, from_lat), (to_long, to_lat))

        # Get driving directions
        geometry = client.directions(coords)['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)

        # Plot driving distance
        plot_map = folium.Map(location=[from_lat, from_long], zoom_start=6, control_scale=True)

        # Plot markers
        folium\
            .Marker([from_lat, from_long], popup=f'From: {from_name} - To: {to_name} Distance: {driving_distance} km')\
            .add_to(plot_map)
        folium.Marker([to_lat, to_long], popup=f'To: {to_name} - From: {from_name} Distance:{driving_distance} km')\
            .add_to(plot_map)

        folium.GeoJson(decoded).add_to(plot_map)

        plot_map.save('map.html')

        return plot_map

    @staticmethod
    def plot_point_map(lat, long, name):
        """
        Plot point on a map
        :param lat: latitude
        :param long: longitude
        :param name: Name
        :return: None
        """

        client = ors.Client(key='___ENTER_API_KEY____')
        # Set location coordinates in longitude,latitude order
        coords = ((long, lat), (long, lat))

        # Get driving directions
        geometry = client.directions(coords)['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)

        # Plot driving distance
        plot_map = folium.Map(location=[lat, long], zoom_start=6, control_scale=True)

        # Plot markers
        folium \
            .Marker([lat, long], popup=f'Name: {name} - Latitude: {lat} - Longitude: {long}') \
            .add_to(plot_map)

        folium.GeoJson(decoded).add_to(plot_map)

        plot_map.save('map.html')

        return plot_map

    @staticmethod
    def plot_heat_map(df, title, warehouse_min_latitude, warehouse_max_longitude):
        """
        Plot heat map
        :param df: Dataframe
        :param title: Title of the plot
        :param warehouse_min_latitude: Warehouse min latitude
        :param warehouse_max_longitude: Warehouse max longitude
        :return: None
        """
        fig = px.density_mapbox(df,
                                lat='latitude',
                                lon='longitude',
                                z='quantity',
                                radius=10,
                                center=dict(lat=warehouse_min_latitude + 5, lon=warehouse_max_longitude - 2),
                                zoom=0,
                                mapbox_style="stamen-terrain")

        fig.update_layout(title=title, title_x=0.5)

        lat_foc = warehouse_min_latitude + 5
        lon_foc = warehouse_max_longitude - 2

        fig.update_layout(geo=dict(projection_scale=10, center=dict(lat=lat_foc, lon=lon_foc),))
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width=1500)

        # Center map
        fig.update_layout(mapbox_center_lat=lat_foc)
        fig.update_layout(mapbox_center_lon=lon_foc)

        # Zoom in
        fig.update_layout(mapbox_zoom=4)

        fig.show()

    @staticmethod
    def plot_transportation_cost_distribution(df, title):
        """
        Plot transportation cost distribution
        :param df: Dataframe
        :param title: Title of the plot
        :return: None
        """
        fig = px.histogram(df,
                           x="transportation_cost",
                           color="transportation",
                           marginal="box",
                           hover_data=df.columns,
                           title=title)

        fig.update_layout(
            xaxis_title="Transportation cost (kg) per km",
            yaxis_title="Count",
            legend_title="Transportation"
        )
        fig.show()
