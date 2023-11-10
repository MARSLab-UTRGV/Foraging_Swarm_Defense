#ifndef PHEROMONE_H
#define PHEROMONE_H

#include <argos3/core/utility/math/vector2.h>

using namespace std;

/*****
 * Implementation of the iAnt Pheromone object used by the iAnt CPFA. iAnts build and maintain a list of these pheromone waypoint objects to use during
 * the informed search component of the CPFA algorithm.
 *****/
class Pheromone {

    public:

        /* constructor function */
        Pheromone(      argos::CVector2 newLocation, std::vector<argos::CVector2> newTrail, argos::Real newTime, 
                        argos::Real newDecayRate, size_t density, bool fake, std::string creator_id);

        /* public helper functions */
        void                         Update(argos::Real time);
        void                         UpdateLocation(argos::CVector2  location); //qilu 09/12/2016
        void                         Deactivate();
        argos::CVector2              GetLocation();
        std::vector<argos::CVector2> GetTrail();
        argos::Real                  GetWeight();
        size_t                       GetResourceDensity();
        bool                          IsActive();
        bool                         IsMisleading();
        std::string                  GetCreatorId();
        argos::Real                  GetEstTravelTime();
        void                         SetReturned(bool val);
        bool                         HasReturnedARobot();
        void                         SetEstTravelTime(argos::Real estTravel);
        argos::CVector2              location;
        size_t ResourceDensity;

	private:
        
        /* pheromone position variables */

        argos::Real                  GetBaseTravelTime();
        std::vector<argos::CVector2> trail;
        /* pheromone component variables */
        argos::Real lastUpdated;
        argos::Real decayRate;
        argos::Real weight;
        argos::Real threshold;
        bool isAtkPheromone;
        std::string creator_id;
        argos::Real est_travel_time;
        bool returned;          // bool flag set when a robot has returned from traveling the trail
};

#endif //PHEROMONE_H