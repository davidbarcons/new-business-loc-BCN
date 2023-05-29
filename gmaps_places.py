import googlemaps
from pyproj import Transformer
from shapely.geometry import Point
import numpy as np
from tqdm.notebook import tqdm

class gmaps_places:
            
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
                radius = 100,
                type = 'restaurant',
                #pen_now = True
                )
            
        self.process_search()
        return self.processed_search
 