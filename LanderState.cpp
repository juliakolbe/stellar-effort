#include "LanderState.h"

LanderState::LanderState(long double empty_mass, long double initial_fuel) :
    emptyMass(empty_mass),
    fuelMass(initial_fuel),
    mass(empty_mass + initial_fuel),
    altitude(0.0),
    velocity(0.0, 0.0),
    acceleration(0.0, 0.0) {}