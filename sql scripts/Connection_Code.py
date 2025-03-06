import mysql.connector
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
    def __init__(self, host, database, username, password, port=3306):
        self.connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database,
            port=3308
        )
        self.cursor = self.connection.cursor()

        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lander_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                time_elapsed FLOAT,
                altitude FLOAT,
                velocity FLOAT,
                fuel_left FLOAT,
                thrust_force FLOAT,
                mass FLOAT
            )
        ''')
        self.connection.commit()
    
    def insert_lander_state(self, time_elapsed, altitude, velocity, fuel_left, thrust_force, mass):
        # Check if this exact state already exists
        sql_check = '''
        SELECT id FROM lander_data WHERE time_elapsed = %s AND altitude = %s 
        AND velocity = %s AND fuel_left = %s AND thrust_force = %s AND mass = %s
    '''
        values = (time_elapsed, altitude, velocity, fuel_left, thrust_force, mass)
        self.cursor.execute(sql_check, values)
        existing_entry = self.cursor.fetchone()

        if existing_entry:
            print("Entry already exists, skipping insertion.")
        return  # Exit if data already exists
        self.cursor.execute('''
            INSERT INTO lander_data(time_elapsed, altitude, velocity, fuel_left, thrust_force, mass)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (time_elapsed, altitude, velocity, fuel_left, thrust_force, mass))
        self.connection.commit()
    
    def fetch_latest_lander_state(self):
        self.cursor.execute('''
            SELECT time_elapsed, altitude, velocity, fuel_left, thrust_force, mass 
            FROM lander_data 
            ORDER BY time_elapsed DESC 
            LIMIT 1
        ''')
        result = self.cursor.fetchone()
        
        if result:
            return {
                "time_elapsed": result[0],
                "altitude": result[1],
                "velocity": result[2],
                "fuel_left": result[3],
                "thrust_force": result[4],
                "mass": result[5]
            }
        else:
            return None  # No data found
    def close_connection(self):
        self.connection.close()

# Example usage within your simulation
if __name__ == "__main__":
    from Algorithms import LanderState
    host = 'localhost'
    database = 'rocket'
    username = 'root'
    password = '2046'
    port = 3308
    db = DatabaseConnector(host, database, username, password)
    
    data = db.fetch_all_data()
    if data:
        print("Existing data found, processing with Algorithms.py")
        processed_results = LanderState(data)  # Call the function from Algorithms.py
        print("Processing complete:", processed_results)
    else:
        print("No data found, inserting new data.")
        
            # Simulated data (in a real case, integrate with DoomLander)
    db.insert_lander_state(time_elapsed=10, altitude=8000, velocity=-15, fuel_left=600, thrust_force=2200, mass=1200)
    
    db.close_connection()
