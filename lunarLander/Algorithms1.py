import math
from collections import deque

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
    def init(self, empty_mass, initial_fuel, initial_altitude):
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
