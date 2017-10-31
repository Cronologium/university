#include <cmath>
#include <iostream>
#include <string>

#include "Vector.hpp"
#include "Line.hpp"
#include "Geometry.hpp"
#include "Sphere.hpp"
#include "Image.hpp"
#include "Color.hpp"
#include "Intersection.hpp"
#include "Material.hpp"

#include "Scene.hpp"

using namespace std;
using namespace rt;

double imageToViewPlane(int n, int imgSize, double viewPlaneSize) {
    double u = (double)n*viewPlaneSize / (double)imgSize;
    u -= viewPlaneSize / 2;
    return u;
}

const Intersection findFirstIntersection(const Line& ray,
    double minDist, double maxDist) {
    Intersection intersection;

    for (int i = 0; i < geometryCount; i++) {
        Intersection in = scene[i]->getIntersection(ray, minDist, maxDist);
        if (in.valid()) {
            if (!intersection.valid()) {
                intersection = in;
            }
            else if (in.t() < intersection.t()) {
                intersection = in;
            }
        }
    }

    return intersection;
}

int main() {
    Vector viewPoint(0, 0, 0);
    Vector viewDirection(0, 0, 1);
    Vector viewUp(0, -1, 0);

    double frontPlaneDist = 0;
    double backPlaneDist = 1000;

    double viewPlaneDist = 512;
    double viewPlaneWidth = 1024;
    double viewPlaneHeight = 768;

    int imageWidth = 1024;
    int imageHeight = 768;

    Vector viewParallel = viewUp^viewDirection;

    viewDirection.normalize();
    viewUp.normalize();
    viewParallel.normalize();

    Image image(imageWidth, imageHeight);

    //DO STUFF HERE

    for (int i = 0; i < imageWidth; ++i)
        for (int j = 0; j < imageHeight; ++j)
        {
            Line line(
                viewPoint, 
                viewPoint + viewDirection * viewPlaneDist + 
                    viewUp * imageToViewPlane(j, imageHeight, viewPlaneHeight) +
                    viewParallel * imageToViewPlane(i, imageWidth, viewPlaneWidth),
                false
            );
            Intersection intersection = findFirstIntersection(line, frontPlaneDist, backPlaneDist);
            
            
            if (intersection.valid())
            {
                #ifdef USE_LIGHT
                Color color = intersection.geometry()->material().ambient();
                //image.setPixel(i, j, intersection.geometry()->color());
                for (int l = 0; l < lightCount; ++l) {
                    //Sphere *sp;
                    /*for (int s = 0; s < geometryCount; ++s) {
                        if (scene[s] == intersection.geometry()) {
                            sp = scene[s];
                        }
                    }*/
                    Sphere *sp = (Sphere*) intersection.geometry();
                    Vector N = intersection.vec() - sp->center();
                    Vector T = lights[l]->position() - intersection.vec();
                    N.normalize();
                    T.normalize();

                    #ifdef USE_DIFFUSE
                    if (N * T > 0)
                    {
                        //cout << N * T << " ";
                        color += 
                            intersection.geometry()->material().diffuse() *
                            lights[l]->diffuse() * 
                            (N * T);
                    }
                    #endif

                    Vector E = viewPoint - intersection.vec();
                    Vector R = N * (float)(2.0 * (N * T))  - T;
                    E.normalize();
                    R.normalize();
                    
                    #ifdef USE_SPECULAR
                    if (E * R > 0)
                    {
                        color += lights[l]->specular() * intersection.geometry()->material().specular() * (pow(E * R, intersection.geometry()->material().shininess()));
                    }
                    color *= lights[l]->intensity();
                    #endif
                }
                image.setPixel(i, j, color);
                #else
                image.setPixel(i, j, intersection.geometry()->color());
                #endif
            }
        }

    //UNTIL HERE

    image.store("scene.png");

    for (int i = 0; i < geometryCount; i++) {
        delete scene[i];
    }

    return 0;
}
