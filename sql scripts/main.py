from Connection_Code import DatabaseConnector
from Algorithms import DoomLander

if __name__ == "__main__":
    # Database connection details
    host = '127.0.0.1'
    database = 'rocket'
    username = 'root'
    password = '2046'
    port = 3308  # Ensure correct port

    db = DatabaseConnector(host, database, username, password, port)

    # Fetch latest lander state from MySQL
    lander_data = db.fetch_latest_lander_state()

    if lander_data:
        print("Fetched latest lander state from database:", lander_data)

        # Initialize DoomLander with fetched data
        doom_lander = DoomLander(1200.0, lander_data["fuel_left"], lander_data["altitude"])
        doom_lander.init_from_db(lander_data)

        # Run the simulation
        while not doom_lander.has_landed():
            altitude = doom_lander.get_altitude()
            velocity = doom_lander.get_velocity()
            fuel_left = doom_lander.get_fuel_left()

            # Simple control algorithm
            if altitude < 1000 and velocity > 0:
                doom_lander.queue_thrust_command(2200.0)  # Apply thrust
            else:
                doom_lander.queue_thrust_command(0.0)  # No thrust

            doom_lander.update()

            # Store each step in MySQL
            db.insert_lander_state(
                time_elapsed=lander_data["time_elapsed"] + 1,
                altitude=altitude,
                velocity=velocity,
                fuel_left=fuel_left,
                thrust_force=doom_lander.thruster.thrust_force
            )

        print("Simulation complete. Final landing state stored in the database.")

    else:
        print("No previous lander state found in the database.")

    db.close_connection()