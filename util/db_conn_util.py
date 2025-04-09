import mysql.connector
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(connection_params):
        try:
            connection = mysql.connector.connect(
                host=connection_params['host'],
                port=connection_params['port'],
                database=connection_params['database'],
                user=connection_params['user'],
                password=connection_params['password']
            )
            print("Database connection established successfully")
            return connection
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            raise