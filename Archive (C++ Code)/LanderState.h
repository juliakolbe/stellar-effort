#ifndef LANDER_STATE_H
#define LANDER_STATE_H

#include "Vector2D.h"

class LanderState {
public:
    long double mass;
    long double emptyMass;
    long double fuelMass;
    long double altitude;
    Vector2D velocity;
    Vector2D acceleration;

    // Declare the constructor (without definition)
    LanderState(long double empty_mass, long double initial_fuel);
};

#endif // LANDER_STATE_H