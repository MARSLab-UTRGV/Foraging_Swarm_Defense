// Ryan Luna 12/28/22

#ifndef QZONE_H_
#define QZONE_H_

#include <argos3/core/utility/math/vector2.h>
#include <argos3/core/simulator/entity/floor_entity.h>

#include <source/Base/Food.h>

using namespace argos;
using namespace std;

class QZone {

    public:
        QZone(CVector2 location, size_t radius);
        CVector2    GetLocation();
        CColor      GetColor();
        size_t      GetRadius();

        void RemoveFood(Food foodObj);
        void AddFood(Food newFood);

    protected:
        void        SetLocation(CVector2 newLocation);
        void        SetColor(CColor newColor);
        void        SetRadius(size_t newRadius);

    private:
        CVector2        Location;
        CColor          Color;
        size_t          Radius;
        vector<Food>    QFood;

};

#endif