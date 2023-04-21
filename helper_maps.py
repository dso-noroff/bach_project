import folium
import plotly.express as px


class MapsHelper:

    @staticmethod
    def plot_warehouses(df, title, warehouse_min_latitude, warehouse_max_longitude):
        """
        Plot Warehouses on folium map
        :param df: Dataframe
        :param title: Title of the plot
        :param warehouse_min_latitude: Warehouse min latitude
        :param warehouse_max_longitude: Warehouse max longitude
        :return: None
        """
        m = folium.Map(location=[warehouse_min_latitude + 5, warehouse_max_longitude - 2], zoom_start=6)

        for i in range(len(df)):
            warehouse = df.iloc[i]
            folium.Marker([warehouse['latitude'], warehouse['longitude']], popup=warehouse['name']).add_to(m)

        m.save(title + '.html')
        return m

    @staticmethod
    def plot_warehouse_map(df, title, warehouse_min_latitude, warehouse_max_longitude):
        """
        Plot Warehouses on plotly map
        :param df: Dataframe
        :param title: Title of the plot
        :param warehouse_min_latitude: Warehouse min latitude
        :param warehouse_max_longitude: Warehouse max longitude
        :return: None
        """
        fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='name')

        fig.update_layout(title=title, title_x=0.5)

        lat_foc = warehouse_min_latitude + 5
        lon_foc = warehouse_max_longitude - 2
        fig.update_layout(geo=dict(projection_scale=10, center=dict(lat=lat_foc, lon=lon_foc), ))
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width=1200)
        fig.show()
