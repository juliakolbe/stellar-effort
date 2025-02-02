#include "LunarLander.h"

LunarLander::LunarLander(long double empty_mass, long double initial_fuel, long double initial_altitude)
	: state(empty_mass, initial_fuel) {
	state.altitude = initial_altitude;
}

long double LunarLander::calculateGravitationalAcceleration() const {
	long double r = PhysicsConstants::moon_radius + state.altitude;
	return (PhysicsConstants::G * PhysicsConstants::moon_mass) / (r * r);
}

void LunarLander::update() {
    long double g = calculateGravitationalAcceleration();

    if (!thrustCommands.empty()) {
        long double thrust = thrustCommands.front();
        thrustCommands.pop();
        thruster.thrustForce = thrust;
    }

    long double netAccel = (thruster.thrustForce - g * state.mass) /
        (state.mass - 0.5 * thruster.thrustForce / thruster.burnEfficiency);

    long double dt = PhysicsConstants::time_step;
    state.altitude = state.altitude - state.velocity.y * dt - 0.5 * netAccel * dt * dt;
    state.velocity.y = state.velocity.y + netAccel * dt;

    if (thruster.thrustForce > 0) {
        thruster.applyThrust(state, dt);
    }
}

void LunarLander::queueThrustCommand(long double thrust) {
    thrustCommands.push(thrust);
}

bool LunarLander::hasLanded() const {
    return state.altitude <= 0;
}

bool LunarLander::isLandingSafe() const {
    return std::abs(state.velocity.y) <= PhysicsConstants::safe_landing_velocity;
}