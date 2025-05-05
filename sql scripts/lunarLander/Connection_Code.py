import mysql.connector
from dotenv import load_dotenv
import os

# Dynamically resolve path to creds.env
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, "creds.env")

if not os.path.exists(env_path):
    raise RuntimeError(f"Could not find creds.env at expected path: {env_path}")

# Load .env variables
load_dotenv(env_path)

class DatabaseConnector:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT")),
            ssl_disabled=True
        )
        self.cursor = self.conn.cursor()

    def insert_lander_state(self, session_id, time_elapsed, altitude, velocity, fuel_mass, thrust_force, mass):
        sql = """
        INSERT INTO lander_state (session_id, time_elapsed, altitude, velocity, fuel_mass, thrust_force, mass)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (session_id, time_elapsed, altitude, velocity, fuel_mass, thrust_force, mass)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def fetch_all_states(self):
        self.cursor.execute("SELECT * FROM lander_state")
        return self.cursor.fetchall()

    def get_latest_session_id(self):
        self.cursor.execute("SELECT MAX(session_id) FROM lander_state")
        result = self.cursor.fetchone()
        return result[0] or 0

    def close(self):
        self.cursor.close()
        self.conn.close()
