// Ryan Luna 12/28/22

#include "QuarantineZone.h"

QZone::QZone(CVector2 location, size_t radius):
    Location(location), 
    Radius(radius)
{
    // nothing yet
}

CVector2    QZone::GetLocation()    {return Location;}
CColor      QZone::GetColor()       {return Color;}
size_t      QZone::GetRadius()      {return Radius;}

void        QZone::SetLocation(CVector2 newLocation)    {Location = newLocation;}
void        QZone::SetColor(CColor newColor)            {Color = newColor;}
void        QZone::SetRadius(size_t newRadius)          {Radius = newRadius;}

void        QZone::AddFood(Food newFood)                {QFood.push_back(newFood);}
void        QZone::RemoveFood(Food foodObj){
    
    int i = 0;
    for(Food f : QFood){
        if(f.GetLocation()==foodObj.GetLocation()){
            QFood.erase(QFood.begin()+i);
        }
        i++;
    }
}