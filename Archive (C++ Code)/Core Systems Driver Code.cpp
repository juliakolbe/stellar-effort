#include <iostream>
#include "LunarLander.h"

using namespace std;

int main() {
    // Test values: empty mass, fuel mass, initial altitude
    LunarLander lander(1000, 500, 1000);

    // Run only one update step
    lander.update();

    // Print results
    cout << "Altitude: " << lander.getAltitude() << " meters" << endl;
    cout << "Velocity: " << lander.getVelocity() << " m/s" << endl;
    cout << "Fuel remaining: " << lander.getFuelMass() << " kg" << endl;

    if (lander.isLandingSafe()) {
        cout << "Landing successful!" << endl;
    } else {
        cout << "Crash landing!" << endl;
    }

    return 0;
}