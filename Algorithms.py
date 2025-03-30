from flask import Flask, render_template, request, jsonify
import math
from collections import deque
import os

app = Flask(__name__, template_folder='juliaHTML')

# Vector2D
class Vector2D:
    def init(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

# Physical constants
class PhysicsConstants:
    G = 6.67430e-11
    moon_mass = 7.34767309e22
    moon_radius = 1.740e6
    safe_landing_velocity = 5.0
    time_step = 1.0

# Lander state
class LanderState:
    def init(self, empty_mass, initial_fuel):
        self.empty_mass = empty_mass
        self.fuel_mass = initial_fuel
        self.mass = empty_mass + initial_fuel
        self.altitude = 0.0
        self.velocity = Vector2D()
        self.velocity.init(0.0, 0.0)
        self.acceleration = Vector2D()
        self.acceleration.init(0.0, 0.0)

# Thrust control
class ThrustControl:
    def init(self):
        self.thrust_force = 0.0
        self.burn_efficiency = 1.0
    def apply_thrust(self, lander, duration):
        fuel_used = (self.thrust_force / self.burn_efficiency) *  duration
        lander.fuel_mass -= fuel_used
        lander.mass = lander.empty_mass + lander.fuel_mass

# Lander "Doom"
class DoomLander:
    def __init__(self, empty_mass, initial_fuel, initial_altitude):
        self.state = LanderState()
        self.state.init(empty_mass, initial_fuel)
        self.state.altitude = initial_altitude
        self.thruster = ThrustControl()
        self.thruster.init()
        self.thrust_commands = deque()
    def calculate_gravitational_acceleration(self):
        r = PhysicsConstants.moon_radius + self.state.altitude
        return (PhysicsConstants.G * PhysicsConstants.moon_mass) / (r * r)
    def update(self):
        g = self.calculate_gravitational_acceleration()
        if self.thrust_commands:
            thrust = self.thrust_commands.popleft()
            self.thruster.thrust_force = thrust
        net_accel = (self.thruster.thrust_force - g * self.state.mass) / \
            (self.state.mass - 0.5 * self.thruster.thrust_force / self.thruster.burn_efficiency)
        dt = PhysicsConstants.time_step
        self.state.altitude = self.state.altitude - self.state.velocity.y * dt - 0.5 * net_accel * dt * dt
        self.state.velocity.y = self.state.velocity.y + net_accel * dt
        if self.thruster.thrust_force > 0:
            self.thruster.apply_thrust(self.state, dt)
    def queue_thrust_command(self, thrust):
        self.thrust_commands.append(thrust)
    def has_landed(self):
        return self.state.altitude <= 0
    def is_landing_safe(self):
        return abs(self.state.velocity.y) <= PhysicsConstants.safe_landing_velocity
    def get_altitude(self):
        return self.state.altitude
    def get_velocity(self):
        return self.state.velocity.y
    def get_fuel_mass(self):
        return self.state.fuel_mass

# Serve the GUI
@app.route('/')
def home():
    return render_template('gui.html')

# API to get Lander status
@app.route('/lander_status', methods=['GET'])

# API to apply thrust
@app.route('/apply_thrust', methods=['POST'])
def apply_thrust():
    data = request.json
    thrust = float(data.get('thrust', 0))
    duration = float(data.get('duration', 1.0))
    
    lander.queue_thrust_command(thrust)
    for _ in range(int(duration)):  
        lander.update()

    return jsonify({"message": "Thrust applied", "thrust": thrust, "duration": duration})

if __name__ == '__main__':
    app.run(debug=True)

lander = DoomLander(empty_mass=1200.0, initial_fuel=640.0, initial_altitude=8500.0)

def get_status():
    return {
        "altitude": lander.get_altitude(),
        "velocity": lander.get_velocity(),
        "fuel": lander.get_fuel_mass(),
    }
'''
# Driver Code
def run_lunar_landing_simulation():
    print("Starting Doom Lunar Lander Simulation")
    print("--------------------------------------")
    
    # Configuration parameters
    EMPTY_MASS = 1200.0  # kg
    INITIAL_FUEL = 640.0  # kg
    STARTING_ALTITUDE = 8500.0  # meters
    THRUST_FORCE = 2200.0  # Newtons
    SAFE_DESCENT_ALTITUDE = 1000.0  # meters
    
    # Create and initialize the Doom lander
    doom_lander = DoomLander()
    doom_lander.init(EMPTY_MASS, INITIAL_FUEL, STARTING_ALTITUDE)
    
    print(f"Initial conditions:")
    print(f"  Empty mass: {EMPTY_MASS} kg")
    print(f"  Fuel: {INITIAL_FUEL} kg")
    print(f"  Starting altitude: {STARTING_ALTITUDE} m")
    print(f"  Maximum thrust: {THRUST_FORCE} N")
    print("--------------------------------------")
    
    # Simulation variables
    time_elapsed = 0
    iteration_count = 0  # Added iteration counter
    MAX_ITERATIONS = 10  # Limit the number of iterations

    # Simulation loop
    print("Beginning descent...")
    while not doom_lander.has_landed() and iteration_count < MAX_ITERATIONS:
        # Simple control algorithm
        altitude = doom_lander.get_altitude()
        vertical_velocity = doom_lander.get_velocity()
        remaining_fuel = doom_lander.get_fuel_mass()
        
        # Apply thrust when close to surface or moving too fast
        if ((altitude < SAFE_DESCENT_ALTITUDE and vertical_velocity > 0) or 
            vertical_velocity > 20.0):
            current_thrust = THRUST_FORCE
            thrust_status = "ON"
        else:
            current_thrust = 0.0
            thrust_status = "OFF"
            
        doom_lander.queue_thrust_command(current_thrust)
        doom_lander.update()
        
        # Update time and iteration count
        time_elapsed += PhysicsConstants.time_step
        iteration_count += 1  # Increment iteration counter

        # Report status every 10 seconds of simulation time
        if time_elapsed % 10 < 0.1:
            print(f"Time: {time_elapsed:.1f}s | "
                  f"Altitude: {altitude:.1f}m | "
                  f"Velocity: {vertical_velocity:.2f}m/s | "
                  f"Fuel: {remaining_fuel:.1f}kg | "
                  f"Thrust: {thrust_status}")

    # Check if stopped due to iteration limit
    if iteration_count >= MAX_ITERATIONS:
        print("\nSimulation stopped after 10 iterations.")

    # Final landing report
    final_velocity = doom_lander.get_velocity()
    remaining_fuel = doom_lander.get_fuel_mass()

    print("\nLanding Report:")
    print(f"  Mission time: {time_elapsed:.1f} seconds")
    print(f"  Impact velocity: {abs(final_velocity):.2f} m/s")
    print(f"  Remaining fuel: {remaining_fuel:.1f} kg")

    if doom_lander.is_landing_safe():
        print("\nMission Status: SUCCESS - Doom has landed safely on the lunar surface!")
    else:
        print(f"\nMission Status: FAILURE - Doom has crashed! (Impact velocity exceeded {PhysicsConstants.safe_landing_velocity} m/s)")

# Run the simulation if this file is executed directly
if __name__ == "__main__":
    run_lunar_landing_simulation()
'''
