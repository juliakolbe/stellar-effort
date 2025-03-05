import pyodbc
import os
import importlib.util

# Check if Algorithms.py exists in the same directory
algorithms_path = os.path.join(os.path.dirname(__file__), 'Algorithms.py')
if os.path.exists(algorithms_path):
    spec = importlib.util.spec_from_file_location("Algorithms", algorithms_path)
    Algorithms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(Algorithms)
else:
    print("Warning: Algorithms.py not found in the current directory.")

class DatabaseConnector:
    def __init__(self, server, database, username, password):
        self.connection = pyodbc.connect(
            f'DRIVER={{SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='lander_data' AND xtype='U')
            CREATE TABLE lander_data (
                id INT IDENTITY(1,1) PRIMARY KEY,
                time_elapsed FLOAT,
                altitude FLOAT,
                velocity FLOAT,
                fuel_mass FLOAT,
                thrust_applied FLOAT
            )
        ''')
        self.connection.commit()
    
    def insert_lander_state(self, time_elapsed, altitude, velocity, fuel_mass, thrust_applied):
        self.cursor.execute('''
            INSERT INTO lander_data (time_elapsed, altitude, velocity, fuel_mass, thrust_applied)
            VALUES (?, ?, ?, ?, ?)
        ''', (time_elapsed, altitude, velocity, fuel_mass, thrust_applied))
        self.connection.commit()
    
    def fetch_all_data(self):
        self.cursor.execute("SELECT * FROM lander_data")
        return self.cursor.fetchall()
    
    def close_connection(self):
        self.connection.close()

# Example usage within your simulation
if __name__ == "__main__":
    server = 'your_server_name'
    database = 'your_database_name'
    username = 'your_username'
    password = 'your_password'
    
    db = DatabaseConnector(server, database, username, password)
    
    # Simulated data (in a real case, integrate with DoomLander)
    db.insert_lander_state(time_elapsed=10, altitude=8000, velocity=-15, fuel_mass=600, thrust_applied=2200)
    
    data = db.fetch_all_data()
    for row in data:
        print(row)
    
    db.close_connection()
