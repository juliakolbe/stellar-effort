#ifndef Physics_Constants_H
#define Physics_Constants_H

class PhysicsConstants {
public:
	static constexpr long double G{ 6.67430e-11 };
	static constexpr long double moon_mass{ 7.34767309e22 };
	static constexpr long double moon_radius{ 1.740e6 };
	static constexpr long double safe_landing_velocity{ 5.0 };
	static constexpr long double time_step{ 1.0 };
};

#endif // Physics_Constants_H