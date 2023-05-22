import mysql.connector
from mysql.connector import Error

class database:
    def __init__(self, host_name, user_name, password, db):
        self.host_name = host_name
        self.user_name = user_name
        self.password = password
        self.db = db
        self.create_server_connection()
        self.create_db_connection(self.db) # Connect to the Database

    def create_server_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.password
            )
            print("MySQL Server connection successful")
        except Error as err:
            print(f"Error: '{err}'")

    def create_database(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")

    def create_db_connection(self, db_name):
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.password,
                database=db_name
            )
            print("MySQL Database connection test successful")
            self.connection.close()
        except Error as err:
            print(f"Error: '{err}'")

    def execute_query(self, query):
        self.connection.reconnect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query successful")
            
        except Error as err:
            print(f"Error: '{err}'")
            
        finally:
            # Close the cursor and connection
            cursor.close()
            self.connection.close()

    @staticmethod
    def write_insert_query_from_dict(table, dictionary):
        # Prepare data for the query
        dictionary['vicinity'] = dictionary['vicinity'].replace(",", "")
        vals = ", ".join("'{s}'".format(s=s.replace("'", "''")) if isinstance(s, str) else str(s) for s in dictionary.values())
        keys = ", ".join(str(s) for s in dictionary.keys())
        query = "INSERT INTO {table} ({keys}) VALUES ({vals})".format(table=table, keys=keys, vals=vals)
        return query
    
    def insert_query(self, table, search_result):
        insert_query = self.write_insert_query_from_dict(table, search_result)
        try:
            self.execute_query(insert_query)
        except Error as err:
            print(f"Error: '{err}'")
            
    import mysql.connector

    def execute_select_query(self, select_query):
    
        self.connection.reconnect()
        cursor = self.connection.cursor()

        try:
            # Execute the SELECT query
            cursor.execute(select_query)
            # Fetch all rows from the result set
            rows = cursor.fetchall()
            # Return the rows
            return rows

        except mysql.connector.Error as error:
            print(f"Error reading MySQL query: {error}")

        finally:
            # Close the cursor and connection
            cursor.close()
            self.connection.close()
