#include "Sphere.hpp"
#include <math.h>

using namespace rt;

Intersection Sphere::getIntersection(const Line& line, double minDist, double maxDist) {
    Intersection in;

    // ADD CODE HERE
    double a = line.dx().x();
    double b = line.dx().y();
    double c = line.dx().z();

    double d = line.x0().x();
    double e = line.x0().y();
    double f = line.x0().z();

    double x = _center.x();
    double y = _center.y();
    double z = _center.z();

    double A = a * a + b * b + c * c;
    double B = 2 * ((a * (d - x) + b * (e - y) + c * (f - z)));
    double C = x * x + y * y + z * z + d * d + e * e + f * f - 2 * (x * d + y * e + f * z) - _radius * _radius;

    double delta = B * B - 4 * A * C;

    if (delta >= 0)
    {
        double t = -500;
        if (delta > 0) // two intersections, return smallest t
        {
            double sq_delta = sqrt(delta);
            double t1 = (- B + sq_delta) / (2 * A);
            double t2 = (- B - sq_delta) / (2 * A);
            t = ((t1 < t2) ? (t1) : (t2));

        }
        else if (!delta) // just one intersection, line is tangent to sphere
        {
            t = (- B) / (2 * A);
        }
        Intersection intersection(true, this, &line,  t);
        in = intersection;
    }
    return in;
}


const Vector Sphere::normal(const Vector& vec) const {
    Vector n = vec - _center;
    n.normalize();
    return n;
}
