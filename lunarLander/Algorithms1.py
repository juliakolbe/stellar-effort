import math
from collections import deque
# Vector2D
class Vector2D:
    def __init__(self, x = 0.0, y = 0.0):
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
        self.burn_efficiency = 1.0
    def apply_thrust(self, lander, duration):
        # check to make sure you have fuel
        if lander.fuel_mass <= 0:
            fuel_used = 0
            lander.fuel_mass = 0
        else:    
            fuel_used = (self.thrust_force / self.burn_efficiency) * (duration)
            lander.fuel_mass -= fuel_used
            lander.mass = lander.empty_mass + lander.fuel_mass
# Lander "Doom"
class DoomLander:
    def __init__(self, empty_mass, initial_fuel, initial_altitude):
        self.state = LanderState(empty_mass, initial_fuel)
        self.state.altitude = initial_altitude
        self.thruster = ThrustControl()
        self.thrust_commands = deque()
    def calculate_gravitational_acceleration(self):
        r = PhysicsConstants.moon_radius + self.state.altitude
        # Add negative sign to make gravity pull downward
        return -1 * (PhysicsConstants.G * PhysicsConstants.moon_mass) / (r * r)
    def update(self):
        g = self.calculate_gravitational_acceleration()
        if self.thrust_commands:
            thrust = self.thrust_commands.popleft()
            self.thruster.thrust_force = thrust
        
        # Calculate net acceleration (positive means upward)
        # Thrust is upward (positive), gravity is downward (negative)
        net_accel = self.thruster.thrust_force / self.state.mass + g
        
        dt = PhysicsConstants.time_step
        
        # First update velocity using current acceleration
        # check to make sure you haven't hit the ground
        if self.state.altitude <= 0:
            self.state.velocity.y = self.state.velocity.y
        else:
            self.state.velocity.y = self.state.velocity.y + net_accel * dt
        
        # Then update altitude using new velocity
        # check to make sure you haven't hit the ground
        if self.state.altitude <= 0:
            self.state.altitude = 0
        else:
            self.state.altitude = self.state.altitude + self.state.velocity.y * dt
        
        # Apply thrust effects on fuel if thrusting
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
