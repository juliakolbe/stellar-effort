#include "ThrustControl.h"

void ThrustControl::applyThrust(LanderState& lander, long double duration) {
	long double fuelUsed = (thrustForce / burnEfficiency) * duration;
	lander.fuelMass -= fuelUsed;
	lander.mass = lander.emptyMass + lander.fuelMass;
}