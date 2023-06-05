import requests
import urllib.parse
import pandas as pd
import googlemaps
from pyproj import Transformer
from shapely.geometry import Point
import numpy as np
from tqdm import tqdm

class gmaps_places:
    """
    Class to make a nearby search in google maps places API, given the geometric bounds within we want to search.
    self.create_grid_coords(self, multipolygon, distance):
        Creates the grid. 
        - border: shapely.geometry.multipolygon.MultiPolygon object describing the border.
        - distance: spacing between grid points.
    self.nearby_search(self, radius):
        It does the "nearby search" at all grid points.
        - radius: radius of the "nearby search". It should be optimized upon the density of places where the search is done.
                Bare in mind that the API returns a maximum of 20 places.
    process_search(self):
        It processes the search results into a dictionary format that we can easily load into our database.
    """
            
    def __init__(self, key, keys_to_store = None):
        #Create the connection to gmaps
        self.keys_to_store = ['place_id', 'name','business_status', 'geometry', 'rating', 'user_ratings_total','price_level', 'vicinity']
        self.client = googlemaps.Client(key=key)
        self.coord_transformer = Transformer.from_crs("WGS84", "EPSG:25831") # Coordinate transformer
        self.coord_transformer_inv = Transformer.from_crs("EPSG:25831", "WGS84") # Inverse coordinate transformer
        if keys_to_store is not None:
            self.keys_to_store = keys_to_store

    def process_search (self):
        self.processed_search = []
        for r in self.search['results']:
            #Check info is complete, then copy search result.
            if all(keys in list(r.keys()) for keys in self.keys_to_store) and r['business_status'] == 'OPERATIONAL':
                pro_dict = r
                pro_dict = {key: pro_dict[key] for key in self.keys_to_store if key in pro_dict}
                #Convert coordinates to our system EPSG:25831
                pro_dict['loc_x'] = int(self.coord_transformer.transform(pro_dict['geometry']['location']['lat'],pro_dict['geometry']['location']['lng'])[0])
                pro_dict['loc_y'] = int(self.coord_transformer.transform(pro_dict['geometry']['location']['lat'],pro_dict['geometry']['location']['lng'])[1])
                del pro_dict['geometry'], pro_dict['business_status']
                self.processed_search.append(pro_dict)
            
    def create_grid_coords(self, multipolygon, distance):
    # multipolygon object that specifies the border of the region in which we want to create the grid
    # Returns a list with the coordinates
        grid_points = []
        for polygon in multipolygon.geoms:
            # Get the bounding box of the polygon
            minx, miny, maxx, maxy = polygon.bounds

            # Calculate the number of points in each dimension
            num_points_x = int((maxx - minx) / distance)
            num_points_y = int((maxy - miny) / distance)

            # Generate the grid of points
            x_coords = np.linspace(minx, maxx, num_points_x)
            y_coords = np.linspace(miny, maxy, num_points_y)
            points = np.meshgrid(x_coords, y_coords)
            points = np.column_stack((points[0].flatten(), points[1].flatten()))

            # Select only the points that fall within the polygon
            polygon_points = [Point(point) for point in points if polygon.contains(Point(point))]
            
            grid_points.extend(polygon_points)
            self.grid_coords = []
            for p in grid_points:
                self.grid_coords.append(self.coord_transformer_inv.transform(int(p.coords.xy[0][0]),int(p.coords.xy[1][0])))  

    def nearby_search (self, radius):
        try:
            grid = self.grid_coords
        except NameError:
            raise NameError("Grid does not exist yet. Use 'create_grid_coords' method first.")
        for loc in tqdm(grid):
            self.search = self.client.places_nearby(
                location= loc,
                radius = radius,
                type = 'restaurant',
                #open_now = True
                ) 
        self.process_search()
        return self.processed_search
 

class bcn_open_data:
    """
    Class to collect data (a full SQL table) from the BCN open data website: https://opendata-ajuntament.barcelona.cat/data/en/dataset
    The method self.get_data(table_id) returns a pandas DataFrame containing all the data in the table.
    ** Check which databases are supported for SQL querying.
    """
    def __init__(self):
        self.url_base = 'https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search_sql?sql='
        self.sql_select_query = """ SELECT * from "table" """

    def convert_sql_query_to_bcnod_url(self, table_id):
        q = self.sql_select_query.replace('table', table_id)
        q = urllib.parse.quote(q)
        return str(self.url_base + q)
    
    def to_numeric(self, dataframe):
        for col in dataframe.columns.tolist():
            try:
                dataframe[col] = dataframe[col].astype(str)
                dataframe[col] = pd.to_numeric(dataframe[col])
            except ValueError:
                dataframe[col] = dataframe[col].astype(str)
                pass
        return dataframe

    def get_data(self, table_id):
        api_url = self.convert_sql_query_to_bcnod_url (table_id)
        response = requests.get(api_url).json()
        df = pd.DataFrame(response['result']['records'])
        return self.to_numeric(df)
    
