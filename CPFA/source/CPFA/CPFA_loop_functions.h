#ifndef CPFA_LOOP_FUNCTIONS_H
#define CPFA_LOOP_FUNCTIONS_H

#include <argos3/core/simulator/loop_functions.h>
#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>
#include <argos3/core/simulator/entity/floor_entity.h>
#include <source/CPFA/CPFA_controller.h>
// #include <source/CPFA/Detractor_controller.h>
#include <argos3/plugins/simulator/entities/cylinder_entity.h>
#include <source/Base/Food.h>	// Ryan Luna 11/10/22
#include <source/Base/Nest.h>	// Ryan Luna 1/24/23
#include <source/Base/Attacker_Nest.h>
#include <cmath>				// Ryan Luna 1/25/23
#include <unordered_map>
#include <unordered_set>
#include <set>


// #include <Python.h>
/***************************************************************************************************/
/**
 * This is a workaround for a keyword naming conflict between some Python headers and QT 5.
 * Solution found here: https://stackoverflow.com/questions/23068700/embedding-python3-in-qt-5
 */

#pragma push_macro("slots")
#undef slots
#include "Python.h"
#pragma pop_macro("slots")

/**
 * NOTE: From ChatGPT
 * 
 * 		This workaround is specific to the compilers that support #pragma push_macro and #pragma pop_macro.
 * 		Most modern compilers like GCC and Clang support these pragmas, but it's something to be aware of
 * 		if you're working in a cross-platform or cross-compiler context.
 */

/***************************************************************************************************/

using namespace argos;
using namespace std;

static const size_t GENOME_SIZE = 7; // There are 7 parameters to evolve

class CPFA_loop_functions : public argos::CLoopFunctions
{

	friend class CPFA_controller;
	friend class Detractor_controller;
	friend class CPFA_qt_user_functions;

	public:

		CPFA_loop_functions();
	   
		void Init(argos::TConfigurationNode &t_tree);
		void Reset();
		void PreStep();
		void PostStep();
		bool IsExperimentFinished();
		void PostExperiment();
		argos::CColor GetFloorColor(const argos::CVector2 &c_pos_on_floor);

		// GA Functions
		
		/* Configures the robot controller from the genome */
		void ConfigureFromGenome(Real* pf_genome);
		/* Calculates the performance of the robot in a trial */
		Real Score();
	
		/**
		 * Returns the current trial.
		 */
		UInt32 GetTrial() const;
	
		/**
		 * Sets the current trial.
		 * @param un_trial The trial number.
		 */
		void SetTrial(UInt32 un_trial);
	
		/* public helper functions */
		void UpdatePheromoneList();
		void SetFoodDistribution();
		void DistributeAtkNests();

		argos::Real getSimTimeInSeconds();

		std::vector<argos::CColor>   TargetRayColorList;

		unsigned int getNumberOfRobots();
        void increaseNumDistributedFoodByOne();
		double getProbabilityOfSwitchingToSearching();
		double getProbabilityOfReturningToNest();
		double getUninformedSearchVariation();
		double getRateOfInformedSearchDecay();
		double getRateOfSiteFidelity();
		double getRateOfLayingPheromone();
		double getRateOfPheromoneDecay();

		vector<pair<CVector2, int>>& GetClusterList();

		void Terminate();

		void CaptureRobotInAtkNest(string id);



		void PushToTrailLog(string bot_id, Pheromone P, Real startTime);
		void PopFromTrailLog(std::string bot_id);
		vector<CVector3> GetAtkNestList();

		CVector2 GetNestLocation();
		// Real GetBotFwdSpeed();

		Pheromone& GetTrailFollowed(std::string id);
		void LogReturn(std::string id, Real time, bool returnedFromTrail);

	protected:
		vector<pair<CVector2, int>> clusterList; // for QT functions

		void setScore(double s);

		argos::CRandom::CRNG* RNG;
        size_t NumDistributedRealFood;		// modified name ** Ryan Luna 11/12/22
		size_t NumDistributedFakeFood;		// Ryan Luna 11/12/22
		size_t TotalDistributedFood;		// Ryan Luna 11/12/22
		size_t MaxSimTime;
		size_t ResourceDensityDelay;
		size_t RandomSeed;
		size_t SimCounter;
		size_t MaxSimCounter;
		size_t VariableFoodPlacement;
		size_t OutputData;
		size_t DrawDensityRate;
		size_t DrawIDs;
		size_t DrawTrails;
		size_t DrawTargetRays;
		size_t FoodDistribution;
		size_t FakeFoodDistribution;	// Ryan Luna 11/13/22
		size_t NumRealFood;			// modified name ** Ryan Luna 11/12/22
		size_t NumFakeFood;			// Ryan Luna 11/12/22
		size_t PowerlawFoodUnitCount;
		size_t PowerlawFakeFoodUnitCount;	// Ryan Luna 11/12/22
		size_t NumberOfClusters;
		size_t ClusterWidthX;
		size_t ClusterWidthY;
		size_t NumFakeClusters;			// Ryan Luna 11/12/22
		size_t FakeClusterWidthX;		// Ryan Luna 11/12/22
		size_t FakeClusterWidthY;		// Ryan Luna 11/12/22
		size_t PowerRank;
		size_t ArenaWidth;
		size_t SimTime; 
		Real curr_time_in_minutes; 
		Real last_time_in_minutes; 

		bool UseFakeFoodDoS;	// Ryan Luna 11/13/22
		bool UseAltDistribution;
		bool UseFakeFoodOnly;
		size_t AltClusterWidth;
		size_t AltClusterLength;

		bool UseMisleadingTrailAttack;

		size_t numRealTrails;
		size_t numFakeTrails;
		size_t ffatk_FalsePositives;
		size_t numQZones;

		// Real BotFwdSpeed;

		Real T_tolerance;

		// vector< std::string, Pheromone > trailLog;

		// make trailLog a tuple with time also included
		vector< std::tuple<std::string, Pheromone, argos::Real, bool> > trailLog;

		vector<Pheromone> inactivePheromoneList;

		Real k;	// correction term for travel time estimation

		/* Result Collection */
		string FilenameHeader;	// Ryan Luna 12/09/22
  
		/* CPFA variables */
		argos::Real ProbabilityOfSwitchingToSearching;
		argos::Real ProbabilityOfReturningToNest;
		argos::CRadians UninformedSearchVariation;
		argos::Real RateOfInformedSearchDecay;
		argos::Real RateOfSiteFidelity;
		argos::Real RateOfLayingPheromone;
		argos::Real RateOfPheromoneDecay;

		/* physical robot & world variables */
		argos::Real FoodRadius;
		argos::Real FoodRadiusSquared;
		argos::Real NestRadius;
		argos::Real NestRadiusSquared;
		argos::Real NestElevation;
		argos::Real SearchRadius;
		argos::Real SearchRadiusSquared;

		argos::Real AtkNestRadius;
		argos::Real AtkNestRadiusSquared;
		size_t NumAtkNests;		

		/* list variables for food & pheromones */
		std::vector<Food>				FoodList;				// Ryan Luna 11/10/22
		vector<Food> 					CollectedFoodList;		// Ryan Luna 11/10/22
        map<string, argos::CVector2> 	FidelityList; 
		std::vector<Pheromone>  	 	PheromoneList; 
		std::vector<argos::CRay3>    	TargetRayList;
		argos::CRange<argos::Real>   	ForageRangeX;
		argos::CRange<argos::Real>   	ForageRangeY;
  
                Real   CollisionTime;
                size_t currCollisionTime; 
                size_t lastCollisionTime; 
                size_t lastNumCollectedFood;
                size_t currNumCollectedFood;
                size_t Num_robots;

		size_t TotalFoodCollected;		// Ryan Luna 11/17/22
		size_t RealFoodCollected;		// Ryan Luna 11/17/22
		size_t FakeFoodCollected;		// Ryan Luna 11/17/22
		size_t DetractorFoodCollected;
		size_t ForagerFoodCollected;

		bool safeTermination = false;

	  	/*TODO: Wondering if it is necessary to make another nest object for the attacker nest... */
		Nest MainNest;					// Ryan Luna 1/24/23
		AtkNest AttackerNest;
      
        vector<size_t>		ForageList;
		argos::CVector2 NestPosition;
		// argos::CVector2 AtkNest1Position;
		// argos::CVector2 AtkNest2Position;
		// argos::CVector2 AtkNest3Position;
		// argos::CVector2 AtkNest4Position;
		vector<argos::CVector2> AtkNestPositions;

		bool terminate;
		bool densify;

		CVector3 ForagingAreaSize;
		bool IsNearRobot(const CVector2& position);

	private:

		/* private helper functions */
		void AlternateFakeFoodDistribution();
		void RandomFoodDistribution();
		void ClusterFoodDistribution();
		void PowerLawFoodDistribution();
		void RandomFakeFoodDistribution();		// Ryan Luna 11/13/22
		void ClusterFakeFoodDistribution();		// Ryan Luna 11/13/22	
		void PowerLawFakeFoodDistribution();	// Ryan Luna 11/13/22
        bool IsOutOfBounds(argos::CVector2 p, size_t length, size_t width);
		bool IsCollidingWithNest(argos::CVector2 p);
		bool IsCollidingWithAtkNest(argos::CVector2 p);		// Ryan Luna 09/20/23
		bool IsCollidingWithFood(argos::CVector2 p);
		CVector3 GenCapturePosition();		// generate a position to move entity to (outside foraging arena) when captured
		CVector3 GenIsoPosition();			// generate a position to move entity to (inside foraging arena) when isolated
		CVector3 GenUnIsoPosition();
		void IsolateBot(std::string id);	// isolate a bot and position it at the generated position (left of environment outside foraging area)
		void UnIsolateBot(std::string bot_id);
		double score;
		int PrintFinalScore;

		bool AllRobotsCaptured();

		bool checkRatio;
		size_t curNumRealTrails;
		size_t curNumFakeTrails;
		vector<pair<Real, pair<size_t, size_t>>> trailRatioList; // (numRealTrails, numFakeTrails)
		size_t ratioCheckFreq;

		bool SetupPythonEnvironment();

		vector<int> RunDBSCAN(std::vector<std::pair<double, double>> dataset);

		PyObject *pyFileName,	*pyModule;
		PyObject *pyDbscan,		*pyCallDbscan,		*pyDbscanArgs;

		Real T_estimate(Real distance, Real velocity);

		vector<pair<string, size_t>> strikeList;
		size_t strikeLimit;
		
		/**
		 * Map of creator IDs to a set of bots that have caused an issuance of a strike to that creator.
		 * After a bot exceeds the est_travel_time, it will continue to exceed it till it returns to the nest.
		 * This way, after a bot exceeds the est_travel_time, repeated strikes aren't issued to the same creator.
		 * 
		 * NOTE: This could potentially be used in place of strikeList, where the size of the set is the number of strikes.
		*/
		std::unordered_map<std::string, std::set<std::string>> strikeMap;

		bool isUsingPheromone;

		bool useDefense;
		bool useReturnBool;
		bool useClustering;
		bool useClusterGraph;

		Real BotFwdSpeed;

		Real alpha;

		struct GraphNode {
			int nodeId;
			std::unordered_set<std::string> creatorIds;
		};

		struct GraphEdge {
			int fromNodeId;
			int toNodeId;
			int weight;
		};

		std::unordered_map<int, GraphNode> graphNodes;
		std::vector<GraphEdge> graphEdges;

		std::unordered_map<int, std::set<int>> clusterMembers; 		// Map of cluster labels to set of PheromoneList indices
		std::unordered_map<string, set<int>> creatorToClusterMap;	// Map of creator IDs to set of associated cluster labels

		void BuildClusterGraph(const std::unordered_map<int, std::set<int>>& clusterMembers, const std::vector<int>& nonClusteredPoints);
		std::set<int> GetNeighbors(int clusterLabel);
		void DFSHelper(int nodeId, std::set<int>& visited);

		size_t IsoFalsePositives;		// incremented when a normal agent is isolated
		size_t falseNegatives;		// incremented when a detractor agent has a strike removed
		size_t numIsolatedBots;
		std::set<std::string> isolatedBots;
		size_t numUnIsolatedBots;
		size_t UnIsoFalsePositives;		// incremented when a detractor is unisolated

		set<string> tmpNameStorage;

		std::vector<std::pair<double, double>> pointData;			// dbscan dataset (dbscan arg)
		vector<int> clusterLabels;									// returned cluster labels from dbscan (indices correspond to indices in PheromoneList)
		std::unordered_map<int, int> trailToClusterMap; 			// Map of PheromoneList index to its cluster label (It is essentially the same thing as clusterLabels but as a key value pair)
		std::vector<int> nonClusteredPoints;						// Vector of PheromoneList indices of points that could not be clustered (noise points)

		Real uniVelocity;

		bool useFeedbackEq;

		bool printed1 = false;

};

#endif /* CPFA_LOOP_FUNCTIONS_H */
