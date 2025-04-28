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
    G = 6.67430e-11  # m^3/(kg s^2)
    moon_mass = 7.34767309e22  # kg
    moon_radius = 1.740e6  # meters
    safe_landing_velocity = 5.0  # m/s
    time_step = 1.0  # seconds

# Lander state
class LanderState:
    def __init__(self, empty_mass, initial_fuel):
        self.empty_mass = empty_mass  # kg
        self.fuel_mass = initial_fuel  # kg
        self.mass = empty_mass + initial_fuel  # kg
        self.altitude = 0.0  # meters
        self.velocity = Vector2D(0.0, 0.0)  # m/s (positive downward)
        self.acceleration = Vector2D(0.0, 0.0)  # m/s^2

# Thrust control
# Thrust control
class ThrustControl:
    def __init__(self):
        self.thrust_force = 0.0  # Newtons
        self.burn_efficiency = 1.0  # N per (kg/s) fuel

    def apply_thrust(self, lander, duration):
        if lander.fuel_mass <= 0:
            fuel_used = 0
            lander.fuel_mass = 0
            self.thrust_force = 0  # No thrust if no fuel
        else:
            fuel_needed = (self.thrust_force / self.burn_efficiency) * duration
            if fuel_needed >= lander.fuel_mass:
                # Not enough fuel for full thrust
                actual_burn_time = (lander.fuel_mass * self.burn_efficiency) / self.thrust_force
                fuel_used = lander.fuel_mass  # Use up all fuel
                lander.fuel_mass = 0
                self.thrust_force = self.thrust_force * (actual_burn_time / duration)  # scale down thrust
            else:
                fuel_used = fuel_needed
                lander.fuel_mass -= fuel_used

        lander.mass = lander.empty_mass + lander.fuel_mass

# Lander control
class DoomLander:
    def __init__(self, empty_mass, initial_fuel, initial_altitude):
        self.state = LanderState(empty_mass, initial_fuel)
        self.state.altitude = initial_altitude
        self.thruster = ThrustControl()
        self.thrust_commands = deque()

    def calculate_gravitational_acceleration(self):
        r = PhysicsConstants.moon_radius + self.state.altitude
        return -1 * (PhysicsConstants.G * PhysicsConstants.moon_mass) / (r * r)

    def update(self):
        g = self.calculate_gravitational_acceleration()
        if self.thrust_commands:
            thrust = self.thrust_commands.popleft()
            self.thruster.thrust_force = thrust
        else:
            self.thruster.thrust_force = 0.0  # No thrust if none commanded

        # Net acceleration: thrust upward (+), gravity downward (-)
        net_accel = self.thruster.thrust_force / self.state.mass + g
        dt = PhysicsConstants.time_step

        # Update velocity first
        if self.state.altitude <= 0:
            self.state.velocity.y = 0
        else:
            self.state.velocity.y = self.state.velocity.y + net_accel * dt

        # Update altitude with corrected kinematics (0.5 * a * dt^2 term added)
        if self.state.altitude <= 0:
            self.state.altitude = 0
        else:
            self.state.altitude = self.state.altitude + self.state.velocity.y * dt + 0.5 * net_accel * dt * dt

        # Update fuel mass if thrusting
        if self.thruster.thrust_force > 0:
            self.thruster.apply_thrust(self.state, dt)

        # Prevent altitude going below surface
        if self.state.altitude < 0:
            self.state.altitude = 0
            self.state.velocity.y = 0

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
