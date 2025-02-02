#ifndef Lunar_Lander_H
#define Lunar_Lander_H

#include "LanderState.h"
#include "ThrustControl.h"
#include "PhysicsConstants.h"
#include <queue>

class LunarLander {
private:
	LanderState state;
	ThrustControl thruster;
	std::queue<long double> thrustCommands;

	long double calculateGravitationalAcceleration() const;

public:
	LunarLander(long double empty_mass, long double initial_fuel, long double initial_altitude);
	
	long double getAltitude() const { return state.altitude; }
    long double getVelocity() const { return state.velocity.y; }
    long double getFuelMass() const { return state.fuelMass; }

	void update();
	void queueThrustCommand(long double thrust);
	bool hasLanded() const;
	bool isLandingSafe() const;
};

#endif // Lunar_Lander_H