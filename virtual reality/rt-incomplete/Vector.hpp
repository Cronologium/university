#include <cmath>

#ifndef RT_VECTOR_INCLUDED
#define RT_VECTOR_INCLUDED

namespace rt {

    class Vector {
    private:
        double _xyz[3];

    public:
        Vector() {
            _xyz[0] = 0;
            _xyz[1] = 0;
            _xyz[2] = 0;
        }

        Vector(double x, double y, double z) {
            _xyz[0] = x;
            _xyz[1] = y;
            _xyz[2] = z;
        }

        Vector(const Vector& v) {
            _xyz[0] = v._xyz[0];
            _xyz[1] = v._xyz[1];
            _xyz[2] = v._xyz[2];
        }

        inline double& x() {
            return _xyz[0];
        }

        inline double& y() {
            return _xyz[1];
        }

        inline double& z() {
            return _xyz[2];
        }

        inline Vector operator + (const Vector& v) const {
            return Vector(_xyz[0] + v._xyz[0],
                _xyz[1] + v._xyz[1],
                _xyz[2] + v._xyz[2]);
        }

        inline Vector& operator += (const Vector& v) {
            _xyz[0] += v._xyz[0];
            _xyz[1] += v._xyz[1];
            _xyz[2] += v._xyz[2];
            return *this;
        }

        inline Vector operator - (const Vector& v) const {
            return Vector(_xyz[0] - v._xyz[0],
                _xyz[1] - v._xyz[1],
                _xyz[2] - v._xyz[2]);
        }

        inline Vector& operator -= (Vector& v) {
            _xyz[0] -= v._xyz[0];
            _xyz[1] -= v._xyz[1];
            _xyz[2] -= v._xyz[2];
            return *this;
        }

        inline double operator * (const Vector& v) const {
            return _xyz[0] * v._xyz[0] + _xyz[1] * v._xyz[1] + _xyz[2] * v._xyz[2];
        }

        inline Vector operator ^ (const Vector& v) const {
            return Vector(_xyz[1] * v._xyz[2] - _xyz[2] * v._xyz[1],
                _xyz[2] * v._xyz[0] - _xyz[0] * v._xyz[2],
                _xyz[0] * v._xyz[1] - _xyz[1] * v._xyz[0]);
        }

        inline Vector operator * (double k) const {
            return Vector(_xyz[0] * k,
                _xyz[1] * k,
                _xyz[2] * k);
        }

        inline Vector& operator *= (double k) {
            _xyz[0] *= k;
            _xyz[1] *= k;
            _xyz[2] *= k;
            return *this;
        }

        inline Vector operator / (double k) const {
            return Vector(_xyz[0] / k,
                _xyz[1] / k,
                _xyz[2] / k);
        }

        inline Vector& operator /= (double k) {
            _xyz[0] /= k;
            _xyz[1] /= k;
            _xyz[2] /= k;
            return *this;
        }

        inline double length() const {
            return sqrt(_xyz[0] * _xyz[0] + _xyz[1] * _xyz[1] + _xyz[2] * _xyz[2]);
        }

        inline double length2() const {
            return _xyz[0] * _xyz[0] + _xyz[1] * _xyz[1] + _xyz[2] * _xyz[2];
        }

        inline double normalize() {
            double norm = length();
            if (norm > 0.0)
            {
                double inv = 1.0 / norm;
                _xyz[0] *= inv;
                _xyz[1] *= inv;
                _xyz[2] *= inv;
            }
            return norm;
        }
    };
}

#endif
