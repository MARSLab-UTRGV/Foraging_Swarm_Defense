#ifndef CPFA_CONTROLLER_H
#define CPFA_CONTROLLER_H

#include <source/Base/BaseController.h>
#include <source/Base/Pheromone.h>
#include <source/CPFA/CPFA_loop_functions.h>
/* Definition of the LEDs actuator */
#include <argos3/plugins/robots/generic/control_interface/ci_leds_actuator.h>

// Ryan Luna 12/28/22
#include <source/Base/QuarantineZone.h>
#include <source/Base/Food.h>

#include <source/Base/Attacker_Nest.h>

using namespace std;
using namespace argos;

static unsigned int num_targets_collected = 0;

class CPFA_loop_functions;

class CPFA_controller : public BaseController {

	public:

		CPFA_controller();

		// CCI_Controller inheritence functions
		void Init(argos::TConfigurationNode &node);
		void ControlStep();
		void Reset();

		bool IsHoldingFood();
		bool IsHoldingFakeFood();	// Ryan Luna 11/12/22
		bool IsUsingSiteFidelity();
		bool IsInTheNest();
		bool IsInTheBadNest();

		Real FoodDistanceTolerance;


		void SetLoopFunctions(CPFA_loop_functions* lf);
  
		size_t     GetSearchingTime();//qilu 09/26/2016
		size_t      GetTravelingTime();//qilu 09/26/2016
		string      GetStatus();//qilu 09/26/2016
		string 		GetDetractorStatus();
		void		SetAsDetractor();
		void		SetAsCaptured();
		bool 		IsCaptured();
		void		SetAsIsolated();
		bool 		IsIsolated();
		size_t      startTime;//qilu 09/26/2016
		void        SetUnIsolated();

		/* quarantine zone functions */		// Ryan Luna 12/28/22
		void ClearZoneList();
		void ClearLocalFoodList();
		void AddZone(QZone newZone);
		void AddLocalFood(Food newFood);
		void RemoveZone(QZone Z);
		void RemoveLocalFood(Food F);
		bool TargetInQZone(CVector2 target);

		void SetDetractorStartPosition(CVector2 newStartPosition);	// to be set in the loop functions

	private:

		/* quarantine zone variables */		// Ryan Luna 12/28/22
		vector<QZone>	QZoneList;
		vector<Food>	LocalFoodList;

		Food FoodBeingHeld;		// Ryan Luna 1/24/23

  		string 			controllerID;//qilu 07/26/2016

		CPFA_loop_functions* LoopFunctions;
		argos::CRandom::CRNG* RNG;

		/* pheromone trail variables */
		std::vector<argos::CVector2> TrailToShare;
		std::vector<argos::CVector2> TrailToFollow;
		std::vector<argos::CRay3>    MyTrail;

		/* robot position variables */
		argos::CVector2 SiteFidelityPosition;
  		bool			 updateFidelity; //qilu 09/07/2016
  
		vector<CRay3> myTrail;
		CColor        TrailColor;

		bool isInformed;
		bool isWronglyInformed;
		bool isHoldingFood;
		bool isHoldingFakeFood;		// Ryan Luna 11/12/22
		bool isUsingSiteFidelity;
		bool isGivingUpSearch;
		bool QZoneStrategy;		// to turn ON/OFF Quarantine Zones

		CVector2 AtkNestPos;
  
		size_t ResourceDensity;
		size_t MaxTrailSize;
		size_t SearchTime;//for informed search
		size_t BadFoodCount;	// Ryan Luna 01/30/23
		size_t BadFoodLimit;	// Ryan Luna 01/30/23
		QZone* CurrentZone;		// Ryan Luna 01/30/23
		bool UseQZones;			// Ryan Luna 02/05/23
		size_t MergeMode;

		bool UseMTAtk;
  
		size_t           searchingTime; //qilu 09/26
		size_t           travelingTime;//qilu 09/26

		Real	FFdetectionAcc;
		Real    RFdetectionAcc;

		/* Detractor related stuff */
		bool captured;
		size_t captureTime;
        
  
		/* iAnt CPFA state variable */
		enum CPFA_state {
			DEPARTING = 0,
			SEARCHING = 1,
			RETURNING = 2,
			SURVEYING = 3,
			CAPTURED  = 4,				// new CPFA state for defined behavior after being captured
			ISOLATED  = 5,				// new CPFA state for defined behavior after being isolated
		} CPFA_state;
		
		enum Detractor_state {
			_HOME_			= 0,			// robot is at its home (attacker) nest
			_DEPARTING_ 	= 1,			// departing from the attacker nest to the defender nest
			_DELIVERING_	= 2,			// delivering fake food and deploying false pheromone trail
			_RETURNING_		= 3,			// returning to the attacker nest from the defender nest after delivering fake food
		}	Detractor_state;

		bool isDetractor;					// boolean to set at initialization to determine if robot is a detractor or not
		argos::CVector2 badNestPos;			// location of the attacker nest (used when laying pheromone trails back to bad nest position.

		/* iAnt CPFA state functions */
		void CPFA();
		void Departing();
		void Searching();
		void Returning();
		void Surveying();
		void Captured();
		void Isolated();

		/* iAnt Detractor state functions */
		void Detract();
		void Home_d();
		void Departing_d();
		void Delivering_d();
		void Returning_d();

		/* CPFA/Detractor helper functions */
		void SetRandomSearchLocation();
		void SetHoldingFood();
		void SetLocalResourceDensity();
		void SetFidelityList(argos::CVector2 newFidelity);
		void SetFidelityList();
		bool SetTargetPheromone();
		bool TargetOutOfBounds(CVector2 p);

		void SetInitAtkNestPos(CVector2 P);

		argos::Real GetExponentialDecay(argos::Real value, argos::Real time, argos::Real lambda);
		argos::Real GetBound(argos::Real value, argos::Real min, argos::Real max);
		argos::Real GetPoissonCDF(argos::Real k, argos::Real lambda);

		void UpdateTargetRayList();

		CVector2 previous_position;

		string results_path;
		string results_full_path;
		bool isUsingPheromone;
		bool returnedFromTrail;
		bool isCaptured;
		bool isIsolated;
		bool randomizeAtkNest;

		bool reachedInformedTarget;

		Real footbotRadius = 0.085;		// from argos documentation

		unsigned int survey_count;
		/* Pointer to the LEDs actuator */
        CCI_LEDsActuator* m_pcLEDs;
};

#endif /* CPFA_CONTROLLER_H */
