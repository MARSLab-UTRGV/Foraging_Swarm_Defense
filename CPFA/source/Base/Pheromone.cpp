#include "Pheromone.h"

/*****
 * The  pheromone needs to keep track of four things:
 *
 * [1] location of the waypoint
 * [2] a trail to the nest
 * [3] simulation time at creation
 * [4] pheromone rate of decay
 *
 * The remaining variables always start with default values.
 *****/

/*TODO: make "smart" pheromone trails (creator_id, max_return_time, no_return_flag)*/
Pheromone::Pheromone(   argos::CVector2              newLocation,
                        std::vector<argos::CVector2> newTrail,
                        argos::Real                  newTime,
                        argos::Real                  newDecayRate,
                        size_t                       density,
                        bool                         fake,
                        std::string                  creator_id):
                        
                        /* standard initializations */
                        returned(false),        // flag set when a robot has returned from traveling the trail
                        weight(1.0),            // pheromone is at full strength when created
                        threshold(0.001),       // pheromone is considered inactive when weight < threshold
                        est_travel_time(0.0)    // default is 0 (not sure if we need to keep track of this here)
{
    if (fake){
        /* required initializations */
        isAtkPheromone = true;
        location    = newLocation;
        trail       = newTrail;
        lastUpdated = newTime;
        decayRate   = newDecayRate;
        ResourceDensity = density;
        this->creator_id  = creator_id;
        // cout << "In Pheromone.cpp: Trail to attacker nest created..." << endl;
    }else{
        /* required initializations */
        isAtkPheromone = false;
        location    = newLocation;
        trail       = newTrail;
        lastUpdated = newTime;
        decayRate   = newDecayRate;
        ResourceDensity = density;
        this->creator_id  = creator_id;
        // cout << "In Pheromone.cpp: Trail to real resource created..." << endl;
    }
}

bool Pheromone::IsMisleading(){
    return isAtkPheromone;
}

/*****
 * The pheromones slowly decay and eventually become inactive. This simulates
 * the effect of a chemical pheromone trail that dissipates over time.
 *****/
void Pheromone::Update(argos::Real time) {
    /* pheromones experience exponential decay with time */
    weight *= exp(-decayRate * (time - lastUpdated));
    lastUpdated = time;
}

void Pheromone::UpdateLocation(argos::CVector2  location){ //qilu 09/12/2016


}
/*****
 * Turns off a pheromone and makes it inactive.
 *****/
void Pheromone::Deactivate() {
    weight = 0.0;
}

/*****
 * Return the pheromone's location.
 *****/
argos::CVector2 Pheromone::GetLocation() {
    return location;
}

/*****
 * Return the trail between the pheromone and the nest.
 *****/
std::vector<argos::CVector2> Pheromone::GetTrail() {
    return trail;
}

/*****
 * Return the weight, or strength, of this pheromone.
 *****/
argos::Real Pheromone::GetWeight() {
	return weight;
}
size_t  Pheromone::GetResourceDensity(){
    return ResourceDensity;
}

/*****
 * Is the pheromone active and usable?
 * TRUE:  weight >  threshold : the pheromone is active
 * FALSE: weight <= threshold : the pheromone is not active
 *****/
bool Pheromone::IsActive() {
	return (weight > threshold);
}

/*****
 * Return the ID of the robot that created this pheromone.
 *****/
std::string Pheromone::GetCreatorId() {
    return creator_id;
}

/*****
 * Return the maximum amount of time any robot has spent traveling & returning this trail (as long as they returned).
 *****/
argos::Real Pheromone::GetEstTravelTime() {
    return est_travel_time;
}

void Pheromone::SetEstTravelTime(argos::Real estTravel){
    est_travel_time = estTravel;
}

/*****
 * Set the returned flag to true.
 *****/
void Pheromone::SetReturned(bool val) {
    returned = val;
}

/*****
 * Has a robot returned from traveling this trail?
 *****/
bool Pheromone::HasReturnedARobot() {
    return returned;
}

void Pheromone::AddTraveler(pair<string, argos::Real> id_time) {
    traveler_list.push_back(id_time);
}

bool Pheromone::RemoveTraveler(string robot_id) {
    for (size_t i = 0; i < traveler_list.size(); i++) {
        if (traveler_list[i].first == robot_id) {
            traveler_list.erase(traveler_list.begin() + i);
            return true;
        }
    }
    return false;   // robot_id was not found in the list
}

/*****
 * Return the list of robots that are currently using this trail.
 *****/
// TODO: Might want to let this return a const reference to the list instead of a copy (just to optimize memory usage)
vector<pair<string, argos::Real>> Pheromone::GetTravelerList() {
    return traveler_list;
}