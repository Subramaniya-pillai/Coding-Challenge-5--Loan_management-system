import configparser

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file):
        config = configparser.ConfigParser()
        config.read(property_file)
        
        return {
            'host': config.get('database', 'host'),
            'port': config.getint('database', 'port'),
            'database': config.get('database', 'name'),
            'user': config.get('database', 'username'),
            'password': config.get('database', 'password')
        }