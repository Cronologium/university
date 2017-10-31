#include "Vector.hpp"
#include "Line.hpp"
#include "Intersection.hpp"
#include "Geometry.hpp"
#include "Material.hpp"

#ifndef RT_SPHERE_INCLUDED
#define RT_SPHERE_INCLUDED

namespace rt {

    class Sphere : public Geometry {
    private:
        Vector _center;
        double _radius;

    public:
        Sphere(const Vector& center, double radius, const Material& material)
            : Geometry(material) {
            _center = Vector(center);
            _radius = radius;
        }

        Sphere(double x, double y, double z, double radius, double r, double g, double b)
            : Geometry(Color(r, g, b)) {
            _center = Vector(x, y, z);
            _radius = radius;
        }

        Sphere(double x, double y, double z, double radius,
            double ar, double ag, double ab,
            double dr, double dg, double db,
            double sr, double sg, double sb,
            int sh)
            : Geometry(Material(ar, ag, ab, dr, dg, db, sr, sg, sb, sh)) {
            _center = Vector(x, y, z);
            _radius = radius;
        }

        ~Sphere() {
        }

        virtual Intersection getIntersection(const Line& line,
            double minDist,
            double maxDist);

        inline double& radius() {
            return _radius;
        }

        inline Vector& center() {
            return _center;
        }

        virtual const Vector normal(const Vector& vec) const;
    };
}

#endif
