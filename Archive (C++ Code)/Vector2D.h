#ifndef Vector2D_H
#define Vector2D_H

#include <cmath>

class Vector2D {
public:
	long double x, y;
	
	Vector2D(long double x = 0.0, long double y = 0.0) : x(x), y(y) {}

	long double magnitude() const {
		return std::sqrt(x * x + y * y);
	}
};

#endif // Vector2D_H