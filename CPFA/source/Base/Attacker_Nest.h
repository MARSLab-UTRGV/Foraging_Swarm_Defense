#ifndef ATTACKER_NEST_H_
#define ATTACKER_NEST_H_

#include <map> //qilu 09/11/2016
#include <argos3/core/utility/math/vector2.h>
//#include <argos3/core/utility/math/ray3.h>
#include <argos3/core/utility/logging/argos_log.h>
#include "Pheromone.h"
#include "Food.h"       // Ryan Luna 11/10/22
#include "QuarantineZone.h" // Ryan Luna 1/24/23
using namespace argos;
using namespace std;

/*****
 * Implementation of the iAnt nest object used by the iAnt MPFA. iAnts
 * build and maintain a list of these nest objects.
 *****/
class AtkNest {

	public:
                AtkNest();
                AtkNest(CVector2 location);
                
                vector<Pheromone> PheromoneList;
                map<string, argos::CVector2> FidelityList; //qilu 09/10/2016
                map<string, size_t> DensityOnFidelity; //qilu 09/11/2016
                vector<Food> FoodList;
                size_t num_collected_tags;
                size_t visited_time_point_in_minute;
                CVector2 GetLocation();
                void SetLocation();
                void SetLocation(CVector2 newLocation); //qilu 09/11/2016

                void SetNestIdx(size_t idx);
                size_t GetNestIdx();

                /* Attacker */
                size_t GetNumCapturedRobots();
                void CaptureRobot(string robot_id);
                // void GetNumTransfferedFakeFood();    
        
	private:
                // size_t num_transffered_fake_food;
                vector<string> captured_robot_list;
                CVector2 nestLocation;
                size_t nest_idx;

};

#endif /* ATTACKER_NEST_H_ */
