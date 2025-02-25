#ifndef Thrust_Control_H
#define Thrust_Control_H

#include "LanderState.h"

class ThrustControl {
public:
	ThrustControl() : thrustForce(0.0), burnEfficiency(1.0) {}

	long double thrustForce;
	long double burnEfficiency;

	void applyThrust(LanderState& lander, long double duration);
};

#endif // Thrust_Control_H