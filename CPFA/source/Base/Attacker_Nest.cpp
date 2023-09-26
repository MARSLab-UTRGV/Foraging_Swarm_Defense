#include "Attacker_Nest.h"

/*****
 * The iAnt nest needs to keep track of four things:
 *
 * [1] location
 * [2] nest id 
 * [3] site fidelity
 * [4] pheromone trails
 *
 *****/
	AtkNest::AtkNest(){}
	AtkNest::AtkNest(CVector2   location)
{
    /* required initializations */
	   nestLocation    = location;
    PheromoneList.clear();
    FidelityList.clear();
    DensityOnFidelity.clear(); //qilu 09/11/2016
    FoodList.clear(); //qilu 09/07/2016
    //num_collected_tags=0;
    visited_time_point_in_minute=0;
    nest_idx=-1;
}

/*****
 *****/

/*****
 * Return the nest's location.
 *****/
CVector2 AtkNest::GetLocation() {
    return nestLocation;
}

void AtkNest::SetLocation() {
    nestLocation=CVector2(0.0, 0.0);
}

void AtkNest::SetLocation(CVector2 newLocation) {
    nestLocation = newLocation;
}

void AtkNest:: SetNestIdx(size_t idx){
     nest_idx = idx;
 }
 
size_t AtkNest:: GetNestIdx(){
     return nest_idx;
 } 

size_t AtkNest::GetNumCapturedRobots(){
    return captured_robot_list.size();
}

void AtkNest::CaptureRobot(string robot_id){
    captured_robot_list.push_back(robot_id);
}

