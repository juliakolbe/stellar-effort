import math
from collections import deque

# Vector2D
class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

# Physical constants
class PhysicsConstants:
    G = 6.67430e-11
    moon_mass = 7.34767309e22
    moon_radius = 1.740e6
    safe_landing_velocity = 20.0
    time_step = 1  # Accelerated simulation (10x real-time)

# Lander state
class LanderState:
    def __init__(self, empty_mass, initial_fuel):
        self.empty_mass = empty_mass
        self.fuel_mass = initial_fuel
        self.mass = empty_mass + initial_fuel
        self.altitude = 0.0
        self.velocity = Vector2D(0.0, 0.0)
        self.acceleration = Vector2D(0.0, 0.0)

# Thrust control
class ThrustControl:
    def __init__(self):
        self.thrust_force = 0.0
        self.burn_efficiency = 100.0  # N per (kg/s)

    def apply_thrust(self, lander, duration):
        if lander.fuel_mass <= 0:
            lander.fuel_mass = 0
            self.thrust_force = 0
        else:
            fuel_flow_rate = self.thrust_force / self.burn_efficiency
            fuel_needed = fuel_flow_rate * duration

            if fuel_needed >= lander.fuel_mass:
                actual_burn_time = lander.fuel_mass / fuel_flow_rate
                fuel_used = lander.fuel_mass
                lander.fuel_mass = 0
                self.thrust_force *= (actual_burn_time / duration)
            else:
                fuel_used = fuel_needed
                lander.fuel_mass -= fuel_used

        lander.mass = lander.empty_mass + lander.fuel_mass

# Lander control
class DoomLander:
    def __init__(self, empty_mass, initial_fuel, initial_altitude, db_connector=None, session_id=1):
        self.state = LanderState(empty_mass, initial_fuel)
        self.state.altitude = initial_altitude
        self.thruster = ThrustControl()
        self.thrust_commands = deque()
        self.db_connector = db_connector
        self.session_id = session_id
        self.elapsed_time = 0.0

    def calculate_gravitational_acceleration(self):
        r = PhysicsConstants.moon_radius + self.state.altitude
        return (PhysicsConstants.G * PhysicsConstants.moon_mass) / (r * r)

    def update(self):
        g = self.calculate_gravitational_acceleration()
        dt = PhysicsConstants.time_step

        if self.thrust_commands:
            self.thruster.thrust_force = self.thrust_commands.popleft()
        else:
            self.thruster.thrust_force = 0.0

        if self.thruster.thrust_force > 0:
            initial_mass = self.state.mass
            fuel_flow_rate = self.thruster.thrust_force / self.thruster.burn_efficiency
            fuel_needed = fuel_flow_rate * dt

            if fuel_needed >= self.state.fuel_mass:
                fuel_used = self.state.fuel_mass
                mid_mass = self.state.empty_mass + 0.5 * fuel_used
            else:
                fuel_used = fuel_needed
                mid_mass = self.state.empty_mass + self.state.fuel_mass - 0.5 * fuel_used

            net_accel = (self.thruster.thrust_force - g * initial_mass) / mid_mass
            self.thruster.apply_thrust(self.state, 0.1)  # Burn only 0.1s worth of fuel
        else:
            net_accel = -g

        if self.state.altitude <= 0:
            self.state.altitude = 0
        else:
            self.state.velocity.y += net_accel * dt
            self.state.altitude += self.state.velocity.y * dt + 0.5 * net_accel * dt * dt

        if self.state.altitude < 0:
            self.state.altitude = 0

        self.elapsed_time += dt

        if self.db_connector:
            self.db_connector.insert_lander_state(
                session_id=self.session_id,
                time_elapsed=self.elapsed_time,
                altitude=self.state.altitude,
                velocity=self.state.velocity.y,
                fuel_mass=self.state.fuel_mass,
                thrust_force=self.thruster.thrust_force,
                mass=self.state.mass
            )

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
