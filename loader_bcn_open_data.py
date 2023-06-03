import requests
import urllib.parse
import pandas as pd

class loader_bcn_open_data:
    """
    Class to collect data (a full SQL table) from the BCN open data website.
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
    
