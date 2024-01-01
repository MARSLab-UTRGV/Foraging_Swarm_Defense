#include "CPFA_loop_functions.h"


CPFA_loop_functions::CPFA_loop_functions() :
	RNG(argos::CRandom::CreateRNG("argos")),
	SimTime(0),
    MaxSimTime(0),	//qilu 02/05/2021
	CollisionTime(0), 
	lastNumCollectedFood(0),
	currNumCollectedFood(0),
	TotalFoodCollected(0),		// Ryan Luna 11/17/22
	RealFoodCollected(0),		// Ryan Luna 11/17/22
	FakeFoodCollected(0),		// Ryan Luna 11/17/22
	DetractorFoodCollected(0),
	ForagerFoodCollected(0),
	ResourceDensityDelay(0),
	RandomSeed(GetSimulator().GetRandomSeed()),
	SimCounter(0),
	MaxSimCounter(1),
	VariableFoodPlacement(0),
	OutputData(0),
	DrawDensityRate(4),
	DrawIDs(1),
	DrawTrails(1),
	DrawTargetRays(1),
	FoodDistribution(2),
	FakeFoodDistribution(2),
	NumRealFood(256),			// name modified ** Ryan Luna 11/12/22
	NumFakeFood(0),			// Ryan Luna 11/12/22
	PowerlawFoodUnitCount(256),
	NumberOfClusters(4),
	ClusterWidthX(8),
	ClusterWidthY(8),
	PowerRank(4),
	ProbabilityOfSwitchingToSearching(0.0),
	ProbabilityOfReturningToNest(0.0),
	UninformedSearchVariation(0.0),
	RateOfInformedSearchDecay(0.0),
	RateOfSiteFidelity(0.0),
	RateOfLayingForagerPheromone(0.0),
	RateOfPheromoneDecay(0.0),
	FoodRadius(0.05),
	FoodRadiusSquared(0.0025),
	NestRadius(0.12),
	AtkNestRadius(NestRadius/2),
	NestRadiusSquared(0.0625),
	NestElevation(0.01),
	// We are looking at a 4 by 4 square (3 targets + 2*1/2 target gaps)
	SearchRadius(4.0*FoodRadius),
	SearchRadiusSquared((4.0 * FoodRadius) * (4.0 * FoodRadius)),
	NumDistributedRealFood(0),	// name modified ** Ryan Luna 11/12/22
	NumDistributedFakeFood(0),	// Ryan Luna 11/12/22
	TotalDistributedFood(0),	// name modified ** Ryan Luna 11/12/22
	score(0),
	PrintFinalScore(0),
	UseFakeFoodDoS(false),		// Ryan Luna 11/13/22
	FilenameHeader("\0"),			// Ryan Luna 12/09/22
	terminate(false),
	densify(true),
	numRealTrails(0),
	numFakeTrails(0),
	UseAltDistribution(false),
	AltClusterWidth(0),
	AltClusterLength(0),
	UseFakeFoodOnly(false),
	ffatk_FalsePositives(0),
	numQZones(0),
	k(1),		// initially k = 1 (no effect on estimation)
	useDefense(false),
	useReturnBool(false),
	useClustering(false),
	useClusterGraph(false),
	BotFwdSpeed(0.0),
	alpha(1.0),
	strikeLimit(3),
	IsoFalsePositives(0),
	numIsolatedBots(0),
	useFeedbackEq(false),
	curNumRealTrails(0),
	curNumFakeTrails(0),
	ratioCheckFreq(10),		// check ratio every 10 seconds
	checkRatio(false)
{}

void CPFA_loop_functions::Init(argos::TConfigurationNode &node) {	
 
	argos::CDegrees USV_InDegrees;
	argos::TConfigurationNode CPFA_node = argos::GetNode(node, "CPFA");

	argos::GetNodeAttribute(CPFA_node, "ProbabilityOfSwitchingToSearching", ProbabilityOfSwitchingToSearching);
	argos::GetNodeAttribute(CPFA_node, "ProbabilityOfReturningToNest",      ProbabilityOfReturningToNest);
	argos::GetNodeAttribute(CPFA_node, "UninformedSearchVariation",         USV_InDegrees);
	argos::GetNodeAttribute(CPFA_node, "RateOfInformedSearchDecay",         RateOfInformedSearchDecay);
	argos::GetNodeAttribute(CPFA_node, "RateOfSiteFidelity",                RateOfSiteFidelity);
	argos::GetNodeAttribute(CPFA_node, "RateOfLayingForagerPheromone",      RateOfLayingForagerPheromone);
	argos::GetNodeAttribute(CPFA_node, "RateOfLayingDetractorPheromone", 	RateOfLayingDetractorPheromone);
	argos::GetNodeAttribute(CPFA_node, "RateOfPheromoneDecay",              RateOfPheromoneDecay);
	argos::GetNodeAttribute(CPFA_node, "PrintFinalScore",                   PrintFinalScore);

	UninformedSearchVariation = ToRadians(USV_InDegrees);
	argos::TConfigurationNode settings_node = argos::GetNode(node, "settings");
	
	argos::GetNodeAttribute(settings_node, "MaxSimTimeInSeconds", MaxSimTime);

	MaxSimTime *= GetSimulator().GetPhysicsEngine("dyn2d").GetInverseSimulationClockTick();//qilu 02/05/2021 dyn2d error

	argos::GetNodeAttribute(settings_node, "MaxSimCounter", 				MaxSimCounter);
	argos::GetNodeAttribute(settings_node, "VariableFoodPlacement", 		VariableFoodPlacement);
	argos::GetNodeAttribute(settings_node, "OutputData", 					OutputData);
	argos::GetNodeAttribute(settings_node, "DrawIDs", 						DrawIDs);
	argos::GetNodeAttribute(settings_node, "DrawTrails", 					DrawTrails);
	argos::GetNodeAttribute(settings_node, "DrawTargetRays", 				DrawTargetRays);
	argos::GetNodeAttribute(settings_node, "FoodDistribution", 				FoodDistribution);
	argos::GetNodeAttribute(settings_node, "UseAltDistribution", 			UseAltDistribution);
	argos::GetNodeAttribute(settings_node, "AltClusterWidth", 				AltClusterWidth);
	argos::GetNodeAttribute(settings_node, "AltClusterLength", 				AltClusterLength);
	argos::GetNodeAttribute(settings_node, "UseFakeFoodOnly", 				UseFakeFoodOnly);
	argos::GetNodeAttribute(settings_node, "FakeFoodDistribution", 			FakeFoodDistribution);
	argos::GetNodeAttribute(settings_node, "NumRealFood", 					NumRealFood);					// name modified ** Ryan Luna 11/13/22
	argos::GetNodeAttribute(settings_node, "NumFakeFood", 					NumFakeFood);					// Ryan Luna 11/12/22
	argos::GetNodeAttribute(settings_node, "PowerlawFoodUnitCount", 		PowerlawFoodUnitCount);
	argos::GetNodeAttribute(settings_node, "PowerlawFakeFoodUnitCount", 	PowerlawFakeFoodUnitCount);		// Ryan Luna 11/12/22
	argos::GetNodeAttribute(settings_node, "NumberOfClusters", 				NumberOfClusters);
	argos::GetNodeAttribute(settings_node, "ClusterWidthX", 				ClusterWidthX);
	argos::GetNodeAttribute(settings_node, "ClusterWidthY", 				ClusterWidthY);
	argos::GetNodeAttribute(settings_node, "NumFakeClusters", 				NumFakeClusters);				// Ryan Luna 11/12/22
	argos::GetNodeAttribute(settings_node, "FakeClusterWidthX", 			FakeClusterWidthX);				// Ryan Luna 11/12/22
	argos::GetNodeAttribute(settings_node, "FakeClusterWidthY", 			FakeClusterWidthY);				// Ryan Luna 11/12/22
	argos::GetNodeAttribute(settings_node, "FoodRadius", 					FoodRadius);
    argos::GetNodeAttribute(settings_node, "NestRadius", 					NestRadius);
	argos::GetNodeAttribute(settings_node, "NestElevation", 				NestElevation);
    argos::GetNodeAttribute(settings_node, "NestPosition", 					NestPosition);
	argos::GetNodeAttribute(settings_node, "UseFakeFoodDoS",				UseFakeFoodDoS);				// Ryan Luna 11/13/22
	argos::GetNodeAttribute(settings_node, "FilenameHeader",				FilenameHeader);				// Ryan Luna 12/06/22
    argos::GetNodeAttribute(settings_node, "Densify", 						densify);						// Ryan Luna 02/08/22
	argos::GetNodeAttribute(settings_node, "ForagingAreaSize",				ForagingAreaSize);
	argos::GetNodeAttribute(settings_node, "BotFwdSpeed",					BotFwdSpeed);
	argos::GetNodeAttribute(settings_node, "EstTravelTimeTolerance",		T_tolerance);
	argos::GetNodeAttribute(settings_node, "UseDefenseMethod",				useDefense);
	argos::GetNodeAttribute(settings_node, "UseReturnBoolean",				useReturnBool);
	argos::GetNodeAttribute(settings_node, "UseTrailClustering",			useClustering);
	argos::GetNodeAttribute(settings_node, "UseClusterGraph",				useClusterGraph);
	argos::GetNodeAttribute(settings_node, "FeedbackLoopWeight",			alpha);
	argos::GetNodeAttribute(settings_node, "StrikeLimit",					strikeLimit);
	argos::GetNodeAttribute(settings_node, "UseFeedbackEq",					useFeedbackEq);
	argos::GetNodeAttribute(settings_node, "RatioCheckFreq",				ratioCheckFreq);
	argos::GetNodeAttribute(settings_node, "CheckRatio",					checkRatio);
	FoodRadiusSquared = FoodRadius*FoodRadius;

	argos::TConfigurationNode atk_node = argos::GetNode(node, "detractor_settings");

	argos::GetNodeAttribute(atk_node, "NumAtkNests",					NumAtkNests);
	// argos::GetNodeAttribute(atk_node, "AtkNest1Position",				AtkNest1Position);
	// argos::GetNodeAttribute(atk_node, "AtkNest2Position",				AtkNest2Position);
	// argos::GetNodeAttribute(atk_node, "AtkNest3Position",				AtkNest3Position);
	// argos::GetNodeAttribute(atk_node, "AtkNest4Position",				AtkNest4Position);
	argos::GetNodeAttribute(atk_node, "AtkNestRadius",					AtkNestRadius);

	uniVelocity = BotFwdSpeed;

    //Number of distributed foods ** modified ** Ryan Luna 11/13/22
    if (FoodDistribution == 1){
		if (UseFakeFoodDoS){
			NumDistributedRealFood = ClusterWidthX*ClusterWidthY*NumberOfClusters;
			NumDistributedFakeFood = FakeClusterWidthX*FakeClusterWidthY*NumFakeClusters;
        	TotalDistributedFood = NumDistributedFakeFood+NumDistributedRealFood;
		} else {
			NumDistributedFakeFood = 0;
			NumDistributedRealFood = ClusterWidthX*ClusterWidthY*NumberOfClusters;
			TotalDistributedFood = NumDistributedRealFood;
		}
    } else {
		if (UseFakeFoodDoS){
        	NumDistributedRealFood = NumRealFood;
			NumDistributedFakeFood = NumFakeFood;
			TotalDistributedFood = NumRealFood+NumFakeFood;
		} else {
			NumDistributedRealFood = NumRealFood;
			NumDistributedFakeFood = 0;
			TotalDistributedFood = NumDistributedRealFood;
		}
    }
    

	// calculate the forage range and compensate for the robot's radius of 0.085m
	// argos::CVector3 ArenaSize = GetSpace().GetArenaSize();
	argos::CVector3 ArenaSize = ForagingAreaSize;
	argos::Real rangeX = (ArenaSize.GetX() / 2.0) - 0.085 - 0.1; // ryan luna 12/08/22 ** take away 0.1 so robots avoid getting to close to the wall
	argos::Real rangeY = (ArenaSize.GetY() / 2.0) - 0.085 - 0.1;
	ForageRangeX.Set(-rangeX, rangeX);
	ForageRangeY.Set(-rangeY, rangeY);

	ArenaWidth = ArenaSize[0];
	
	if(abs(NestPosition.GetX()) < -1){ //quad arena
		NestRadius *= sqrt(1 + log(ArenaWidth)/log(2));
		AtkNestRadius = NestRadius/2;
	}else{
		NestRadius *= sqrt(log(ArenaWidth)/log(2));
		AtkNestRadius = NestRadius/2;
	}
	argos::LOG<<"NestRadius="<<NestRadius<<endl;
	argos::LOG<<"AtkNestRadius="<<AtkNestRadius<<endl;

	MainNest.SetLocation(NestPosition);	// Ryan Luna 1/24/23
    
	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");
    Num_robots = footbots.size();
    argos::LOG<<"Number of robots="<<Num_robots<<endl;

	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
		if(c != nullptr) {
			// cout << "Type of BaseController pointer: " << typeid(c).name() << endl;
			CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
			if(c2 != nullptr) {
				c2->SetLoopFunctions(this);

				// cout << "CPFA_controller cast successful" << endl;
			}
			else {
				cout << "CPFA_controller cast failed" << endl;
				cout << "Actual type of c2: " << typeid(c2).name() << endl;
			}
		}
		else {
			cout << "BaseController cast failed" << endl;
		}
	}

   	NestRadiusSquared = NestRadius*NestRadius;
	AtkNestRadiusSquared = AtkNestRadius*AtkNestRadius;

	/**
	 * Distribute atk nests randomly one quadrant of the arena at a time (ignoring innermost subquadrants).
	 */
	DistributeAtkNests();
	
    SetFoodDistribution();
  
	ForageList.clear(); 
	last_time_in_minutes=0;

	if (useDefense && useClustering){
		if (!SetupPythonEnvironment()){
			LOGERR << "ERROR: Failed to setup python environment." << endl;
			// Terminate();
			exit(1);
		}
	}

}

void CPFA_loop_functions::Reset() {
	if(VariableFoodPlacement == 0) {
			RNG->Reset();
	}

    GetSpace().Reset();
    GetSpace().GetFloorEntity().Reset();
    MaxSimCounter = SimCounter;
    SimCounter = 0;
    score = 0;
   
    FoodList.clear();
    CollectedFoodList.clear();	
	PheromoneList.clear();
	FidelityList.clear();
    TargetRayList.clear();

	RealFoodCollected = 0;
	FakeFoodCollected = 0;
	TotalFoodCollected = 0;
    
    SetFoodDistribution();
    
    argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");
	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
		if(c != nullptr) {
			// cout << "Type of BaseController pointer: " << typeid(c).name() << endl;
			CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
			if(c2 != nullptr) {
				MoveEntity(footBot.GetEmbodiedEntity(), c2->GetStartPosition(), argos::CQuaternion(), false);
				c2->Reset();
				// cout << "CPFA_controller cast successful" << endl;
			}
			else {
				cout << "CPFA_controller cast failed" << endl;
				cout << "Actual type of c2: " << typeid(c2).name() << endl;
			}
		}
		else {
			cout << "BaseController cast failed" << endl;
		}
	}
}

void CPFA_loop_functions::PreStep() {
    SimTime++;
    curr_time_in_minutes = getSimTimeInSeconds()/60.0;
    if(curr_time_in_minutes - last_time_in_minutes==1){
        ForageList.push_back(currNumCollectedFood - lastNumCollectedFood);
        lastNumCollectedFood = currNumCollectedFood;
        last_time_in_minutes++;
    }

	UpdatePheromoneList();

	if (fabs(fmod(getSimTimeInSeconds(), ratioCheckFreq)) < EPSILON && checkRatio){

		curNumRealTrails = 0;
		curNumFakeTrails = 0;

		// Get ratio of real trails to fake trails
		for (size_t i = 0; i < PheromoneList.size(); i++){
			if (!PheromoneList[i].IsMisleading()){
				curNumRealTrails++;
			} else {
				curNumFakeTrails++;
			}
		}
		trailRatioList.push_back(make_pair(getSimTimeInSeconds(),make_pair(curNumRealTrails, curNumFakeTrails)));
	}



	// Ryan Luna 11/10/22
	if(GetSpace().GetSimulationClock() > ResourceDensityDelay) {
    	for(size_t i = 0; i < FoodList.size(); i++) {
			if (FoodList[i].GetType() == Food::REAL){
				FoodList[i].SetColor(CColor::BLACK);
			} else {
				FoodList[i].SetColor(CColor::PURPLE);
			}
            
        }
	}
 
    if(FoodList.size() == 0) {
		FidelityList.clear();
		PheromoneList.clear();
        TargetRayList.clear();
    }
}

void CPFA_loop_functions::PostStep() {

	if (useDefense) {

		//TODO: This code is not optimized, I am thinking of using hash tabels to make lookup times faster. Need to look into other optimizations as well.

		// check pheromone list and certain frequency to see if robots are returning within time frame
		argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");

		pointData.clear();
		clusterLabels.clear();
		trailToClusterMap.clear();
		nonClusteredPoints.clear();

		if (useClustering){

			if (PheromoneList.empty()) return; // If there are no pheromones, return

			clusterList.clear(); // clear cluster list for qt functions
			clusterMembers.clear();

			// prepare dataset for clustering
			for (size_t i = 0; i < PheromoneList.size(); i++){
				CVector2 point = PheromoneList[i].GetLocation();
				pointData.push_back(make_pair(point.GetX(), point.GetY()));
			}

			// run dbscan here and not in the loop below to reduce computational complexity.
			// TODO: Look into moving this into the main embedded for loop below so that it is event based (whenever a bot exceeds est_travel_time). 
			// 			Might be able to reduce the number of times we run dbscan.
			clusterLabels = RunDBSCAN(pointData);

			// Each element in clusterLabels corresponds to a PheromoneList index. clusterLables[i] is the cluster label of the pheromone trail at PheromoneList[i]

			for (size_t i = 0; i < clusterLabels.size(); ++i) {
				int label = clusterLabels[i];
				trailToClusterMap[i] = label; // Map trail index to its cluster label

				// maintain creatorToClusterMap
				// TODO: make sure this works the way it needs to. Go thorugh it in detail...
				string creator = PheromoneList[i].GetCreatorId();
				creatorToClusterMap[creator].insert(label);

				// update clusterList for qt functions
				clusterList.push_back(make_pair(PheromoneList[i].GetLocation(), label));

				if (label != -1) { // Ignore noise points
					/**
					 * NOTE: 	clusterMembers is a <key>,<value> pair where the <value> is of type 'set<int>'.
					 * 			
					 * 			A single creator can have multiple trails to the same cluster. 
					 * 
					 * 			e.g. indices 1 and 3 are trails made by fb00 that are part of cluster 2 (key:<2>, value(s):<1,3,4,5,7>).
					 * 
					 * 			Need to make sure that we don't issue multiple strikes to fb00 in this case.
					 */
					clusterMembers[label].insert(i); // Add PheromoneList (clusterLabels) index to the set of its cluster
				} else {
					nonClusteredPoints.push_back(i); // Add PheromoneList (clusterLabels) index to the list of nonClusteredPoints (noise points)
				}
				
			}
		}


		// loop through the traveler lists of each pheromone object
		for (size_t i = 0; i < PheromoneList.size(); i++) {

			vector<pair<string, Real>> traveler = PheromoneList[i].GetTravelerList();

			// Get the cluster label of the current pheromone trail (if using clustering)
			int clusterLabel = -1;
			if (useClustering) clusterLabel = trailToClusterMap[i];

			for (size_t j = 0; j < traveler.size(); j++) {

				// TODO: I think this is ok. I might also want to remove it from the traveler list of the pheromone trail. But this might also decrease the number of trails
				// 			considered when using clustering. Need to look into this more.
				if (isolatedBots.find(traveler[j].first) != isolatedBots.end()) continue; // if the traveler has been isolated, skip it
				
				CVector2 trailPos = PheromoneList[i].GetLocation();
				Real trailLength = sqrt( pow(NestPosition.GetX() - trailPos.GetX(), 2) + pow(NestPosition.GetY() - trailPos.GetY(), 2) );
				Real d = trailLength * 2;	// multiply by 2 to get distance to and from the target location
				Real v = BotFwdSpeed;	

				// get current travel time (sim_time - start_time)
				Real T_current = getSimTimeInSeconds() - traveler[j].second;

				/**
				 * If the robot has taken longer than the expected time to return to the nest, we will begin to issue strikes on trail creators
				 */

				if (T_current > (T_estimate(d,v) * T_tolerance)){

					/********************************************* BASE DEFENSE ********************************************************/

					if (!useClustering){

						/**
						 * For the base defense method, we are only giving strikes to trail creators who's travelers have exceeded the estimated travel time.
						 */

						bool found = false;
						string creator = PheromoneList[i].GetCreatorId();

						// Check if the traveler has already been processed for this creator and that it hasn't been isolated
						if (isolatedBots.find(creator) == isolatedBots.end())
							if (strikeMap[creator].find(traveler[j].first) == strikeMap[creator].end())
								strikeMap[creator].insert(traveler[j].first);

					/******************************************** CLUSTER DEFENSE *******************************************************/

					} else if (useClustering && !useClusterGraph){

						if (clusterLabel == -1) {
							
							string creator = PheromoneList[i].GetCreatorId();

							if (isolatedBots.find(creator) == isolatedBots.end()) // if the creator is not already isolated
								if (strikeMap[creator].find(traveler[j].first) == strikeMap[creator].end()) // AND if the traveler has not already been processed for this creator
									strikeMap[creator].insert(traveler[j].first);

						} else {

							// Iterate over all pheromone trail indices in the cluster specified by 'clusterLabel'
							for (int trailIndex : clusterMembers[clusterLabel]) {

								// check if this trail has returned a robot, if it has, don't isolate its creator (return bool)
								// if (PheromoneList[trailIndex].HasReturnedARobot()) continue;

								// Retrieve the creator ID of the current pheromone trail
								string creator = PheromoneList[trailIndex].GetCreatorId();

								// Check if the traveler has already been processed for this creator and that it hasn't been isolated
								if (isolatedBots.find(creator) == isolatedBots.end())
									if (strikeMap[creator].find(traveler[j].first) == strikeMap[creator].end())
										strikeMap[creator].insert(traveler[j].first);
								
							}
						}
						

					/****************************************** CLUSTER GRAPH DEFENSE ***************************************************/

					} else if (useClustering && useClusterGraph){

						BuildClusterGraph(clusterMembers, nonClusteredPoints);

						int nodeId; // Identifier for the node in the graph

						if (clusterLabel != -1) {

							// The trail is part of a cluster
							nodeId = clusterLabel;

						} else {

							// The trail is a noise point, find its unique identifier
							auto noisePointIt = std::find(nonClusteredPoints.begin(), nonClusteredPoints.end(), i);

							if (noisePointIt != nonClusteredPoints.end()) {

								int noisePointIndex = std::distance(nonClusteredPoints.begin(), noisePointIt);
								nodeId = -(noisePointIndex + 1);

							} else {
								continue; // Noise point not found in nonClusteredPoints maybe need error handling here?
							}
    					}

						// Get the neighbors of the current node (also includes the current node)
						std::set<int> neighbors = GetNeighbors(nodeId);

						// The unordored_set allows us to keep a unique list of elements with no duplicates
						std::unordered_set<std::string> creatorList;

						// Iterate over the neighbors
						for (int neighborId : neighbors) {

							// Get the cluster members of the neighbor
							std::set<int> neighborMembers = clusterMembers[neighborId];

							// Iterate over the cluster members of the neighbor and insert each one into the creatorList, creating a unique list with no duplicates
							for (int trailIndex : neighborMembers) { 
								// if (PheromoneList[trailIndex].HasReturnedARobot()) continue; // skip trails that have returned a robot (return bool)
								creatorList.insert(PheromoneList[trailIndex].GetCreatorId()); 
							}
						}

						// Iterating over a unique creatorList where there is only one entry per creator (no duplicates)
						for (const auto& creator : creatorList){

							if (creator == "fb13" && traveler[j].first == "fb22" && !printed1){
								// printed1 = true;
								// LOGERR << "fb22 traveling on fb13 trail: Pheromone[" << i << "], Label: " << clusterLabel << endl;
								// LOGERR << "fb22 traveling on fb13 trail: Pheromone[" << i << "]" << endl;
							}

							// Check if the traveler has already been processed for this creator and that it hasn't been isolated
							if (isolatedBots.find(creator) == isolatedBots.end())
								if (strikeMap[creator].find(traveler[j].first) == strikeMap[creator].end())
									strikeMap[creator].insert(traveler[j].first);
						}
					}
				}
			}
		}
	}
	/********************************************** STRIKE AND ISOLATE ***************************************************/

	// Check if any bots have reached their strike limit, if so, isolate them and erase them from the strike list.
	// for (size_t i = 0; i < strikeList.size(); i++) {
	// 	if (strikeList[i].second >= strikeLimit) {
	// 		IsolateBot(strikeList[i].first);
	// 		strikeList.erase(strikeList.begin() + i);
	// 	}
	// }
	for (auto it = strikeMap.begin(); it != strikeMap.end(); ) {
		const auto& creator = it->first;
		const auto& strikeSet = it->second;

		if (strikeSet.size() >= strikeLimit && isolatedBots.find(creator) == isolatedBots.end()) {
			
			// if (creator == "fb13"){
			// 	LOG << "Isolating " << creator << " for exceeding strike limit." << endl;
			// 	LOG << "Strike set size: " << strikeSet.size() << endl;
			// 	LOG << "Strike set: ";
			// 	for (const auto& strike : strikeSet){
			// 		LOG << strike << ", ";
			// 	}
			// 	LOG << endl;
			// 	tmpNameStorage = strikeSet;
			// }
			
			IsolateBot(creator);
			isolatedBots.insert(creator);
			it = strikeMap.erase(it);  // Erase and move to the next element safely
		} else {
			++it;  // Move to the next element
		}
	}

	// LOG << "Number of isolated bots: " << isolatedBots.size() << endl;
	// LOG << strikeMap.size() << " bots in strikeMap..." << endl;
}

// Assuming clusterMembers is a map of cluster label to vector of trail indices
// and noisePoints is a vector of noise point indices
void CPFA_loop_functions::BuildClusterGraph(const std::unordered_map<int, std::set<int>>& clusterMembers,
											const std::vector<int>& nonClusteredPoints) {

    int noiseId = -1;

	// Clear previous graph
	graphNodes.clear();
	graphEdges.clear();

    // Process clusters
    for (const auto& [label, indices] : clusterMembers) {
        GraphNode node;
        node.nodeId = label;
        for (int index : indices) {
            node.creatorIds.insert(PheromoneList[index].GetCreatorId());
        }
        graphNodes[node.nodeId] = node;
    }

    // Process non-clustered points (noise points)
    for (int index : nonClusteredPoints) {
        GraphNode node;
        node.nodeId = noiseId--;
        node.creatorIds.insert(PheromoneList[index].GetCreatorId());
        graphNodes[node.nodeId] = node;
    }

    // Create edges
    for (const auto& [id1, node1] : graphNodes) {
        for (const auto& [id2, node2] : graphNodes) {
            if (id1 != id2) {
                // Count common creators
                int commonCreators = 0;
                for (const auto& creator : node1.creatorIds) {
                    if (node2.creatorIds.find(creator) != node2.creatorIds.end()) {
                        ++commonCreators;
                    }
                }

                if (commonCreators > 0) {
                    GraphEdge edge;
                    edge.fromNodeId = id1;
                    edge.toNodeId = id2;
                    edge.weight = commonCreators;
                    graphEdges.push_back(edge);
                }
            }
        }
    }
}

set<int> CPFA_loop_functions::GetNeighbors(int startNodeID){
	std::set<int> visited;
	DFSHelper(startNodeID, visited); // Depth First Search
	return visited;
}

void CPFA_loop_functions::DFSHelper(int nodeId, std::set<int>& visited) {
	
	visited.insert(nodeId);

	// Iterate through the edges
	for (const auto& edge : graphEdges) {
		if (edge.fromNodeId == nodeId) {
			int destinationNodeId = edge.toNodeId;
			// Check if the destination node has not been visited
			if (visited.find(destinationNodeId) == visited.end()) {
				// Recursively call DFSHelper with the destination node
				DFSHelper(destinationNodeId, visited);
			}
		}
	}
}

void CPFA_loop_functions::Terminate(){
	terminate = true;
	LOGERR << "Terminating Simulation..." << endl;
}

bool CPFA_loop_functions::AllRobotsCaptured(){
	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");

	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {

		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());

		if(c != nullptr) {

			CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
			if(c2 != nullptr) {

				if (footBot.GetId().find("fb") != string::npos){

					if (!c2->IsCaptured()) return false;	// there is at least one robot not captured yet...
				}
			}
			else {
				cout << "CPFA_controller cast failed" << endl;
				cout << "Actual type of c2: " << typeid(c2).name() << endl;
			}
		}
		else {
			cout << "BaseController cast failed" << endl;
		}
		
	}

	return true;
}

bool CPFA_loop_functions::IsExperimentFinished() {
	bool isFinished = false;

	if(FoodList.size() == 0 || GetSpace().GetSimulationClock() >= MaxSimTime) {
		isFinished = true;
		// PostExperiment();
	}

	if (AllRobotsCaptured()){
		isFinished = true;
		LOG << "All robots captured. Ending simulation." << endl;
		safeTermination = true;
	}

	if (terminate) {isFinished = true;}

    //set to collected 88% food and then stop
    // if(score >= NumDistributedRealFood){
	// 	isFinished = true;
	// }

	// if(isFinished == true && MaxSimCounter > 1) {
	// 	size_t newSimCounter = SimCounter + 1;
	// 	size_t newMaxSimCounter = MaxSimCounter - 1;
    //     argos::LOG<< "time out..."<<endl; 
	// 	PostExperiment();
	// 	// Reset();

	// 	SimCounter    = newSimCounter;
	// 	MaxSimCounter = newMaxSimCounter;
	// 	isFinished    = false;
	// }

	return isFinished;
}

void CPFA_loop_functions::PostExperiment() {
	  
	printf("%f, %f, %lu\n", score, getSimTimeInSeconds(), RandomSeed);
       
                  
    if (PrintFinalScore == 1) {
        string type="";
        if (FoodDistribution == 0) type = "random";
        else if (FoodDistribution == 1) type = "cluster";
        else type = "powerlaw";
            
        ostringstream num_tag;
        num_tag << NumRealFood; 
              
        ostringstream num_robots;
        num_robots <<  Num_robots;
   
        ostringstream arena_width;
        arena_width << ArenaWidth;
        
        ostringstream quardArena;
        if(abs(NestPosition.GetX())>=1){ //the central nest is not in the center, this is a quard arena
             quardArena << 1;
        }
         else{
             quardArena << 0;
        }
        
		// Now using FilenameHeader defined through the XML ** Ryan Luna 12/09/22
        // header = "./results/"+ type+"_CPFA_r"+num_robots.str()+"_tag"+num_tag.str()+"_"+arena_width.str()+"by"+arena_width.str()+"_quard_arena_" + quardArena.str() +"_";

        unsigned int ticks_per_second = GetSimulator().GetPhysicsEngine("dyn2d").GetInverseSimulationClockTick();//qilu 02/06/2021
        
        argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");

		for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
			argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
			BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
			if(c != nullptr) {
				// cout << "Type of BaseController pointer: " << typeid(c).name() << endl;
				CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
				if(c2 != nullptr) {
					CollisionTime += c2->GetCollisionTime();
					// cout << "CPFA_controller cast successful" << endl;
				}
				else {
					cout << "CPFA_controller cast failed" << endl;
					cout << "Actual type of c2: " << typeid(c2).name() << endl;
				}
			}
			else {
				cout << "BaseController cast failed" << endl;
			}
		}
             
        // ofstream dataOutput( (FilenameHeader+ "iAntTagData.txt").c_str(), ios::app);
        // // output to file
        // if(dataOutput.tellp() == 0) {
        //     dataOutput << "tags_collected, collisions_in_seconds, time_in_minutes, random_seed\n";//qilu 08/18
        // }
    
        // dataOutput << Score() << ", "<<CollisionTime/(2*ticks_per_second)<< ", "<< curr_time_in_minutes << ", " << RandomSeed << endl;
        // dataOutput.close();
    
        // ofstream forageDataOutput((FilenameHeader+"ForageData.txt").c_str(), ios::app);
        // if(ForageList.size()!=0) forageDataOutput<<"Forage: "<< ForageList[0];
        // for(size_t i=1; i< ForageList.size(); i++) forageDataOutput<<", "<<ForageList[i];
        // forageDataOutput<<"\n";
        // forageDataOutput.close();
		
		size_t numIsolatedDetractors = 0;
		size_t numIsolatedForagers = 0;

		if (useDefense){

			LOG << "Total isolated bots (calculated): " << numIsolatedBots - numUnIsolatedBots << endl;

			for (auto& bot : isolatedBots){
				if (bot.find("dt") != string::npos){
					numIsolatedDetractors++;
				}
			}

			for (auto& bot : isolatedBots){
				if (bot.find("fb") != string::npos){
					numIsolatedForagers++;
				}
			}

			LOG << "Total Isolated Detractors: " << numIsolatedDetractors << ", " << "Total Isolated Foragers: " << numIsolatedForagers << endl;

			LOG << "Total Bots Captured: " << AttackerNest.GetNumCapturedRobots() << endl;
		}


		// Write to file ** Ryan Luna 11/17/22
		ofstream DataOut((FilenameHeader+"AttackData.txt").c_str(), ios::app);
		LOG << "Writing to file: " << FilenameHeader+"AttackData.txt" << endl;
		if (DataOut.tellp() == 0){

			DataOut 	<< "Simulation Time (seconds), Total Food Collected, Total Food Collection Rate (per second), " 
							<< "Total Robots Captured, Robots Captured (per second), "
							<< "Real Trails Created, Misleading Trails Created, " 
							<< "Total Collision Time, Random Seed Used, " 
							<< "Total Robots Isolated, Num False Positives, " 
							<< "Total Isolated Detractors, Total Isolated Foragers, " 
							<< "Forager Performance, Detractor Performance" << endl;

							// << "Fake Food Collected, Fake Food Collection Rate (per second), " 
							// << "Real Food Trails Created, Fake Food Trails Created, False Positives, QZones" << endl;
		}

		TotalFoodCollected = RealFoodCollected + FakeFoodCollected;

		DataOut 	<< getSimTimeInSeconds() << ',' << TotalFoodCollected << ',' << TotalFoodCollected/getSimTimeInSeconds() << ','
						<< AttackerNest.GetNumCapturedRobots() << ',' << AttackerNest.GetNumCapturedRobots()/getSimTimeInSeconds() << ','
						<< numRealTrails << ',' << numFakeTrails << ',' 
						<< CollisionTime/(2*ticks_per_second) << ',' << RandomSeed << ','
						<< numIsolatedBots << ',' << IsoFalsePositives << ','
						<< numIsolatedDetractors << ',' << numIsolatedForagers << ','
						<< ForagerFoodCollected << ',' << DetractorFoodCollected << endl;
						
						// << FakeFoodCollected << ',' << FakeFoodCollected/getSimTimeInSeconds() << ','
						// << numRealTrails << ',' << numFakeTrails << ',' << numFalsePositives << ',' << MainNest.GetZoneList().size() << endl;
    }

	ofstream RatioCheck((FilenameHeader+"RatioCheck.txt").c_str(), ios::app);
	LOG << "Writing to file: " << FilenameHeader+"RatioCheck.txt" << endl;
	if (RatioCheck.tellp() == 0){
		RatioCheck << "Time (seconds), Real Trails, Fake Trails" << endl;
	}
	for (const auto& ratio : trailRatioList){
		RatioCheck << ratio.first << ',' << ratio.second.first << ',' << ratio.second.second << endl;
	}

	ofstream TerminateCount ((FilenameHeader+"TerminatedCount.txt").c_str(), ios::app);
	if(terminate){
		TerminateCount	<< 0 << ", ";
	} else {
		TerminateCount	<< 1 << ", ";
	}

	// Close Python environment if initialized
	if (useDefense && Py_IsInitialized()) {
		Py_Finalize(); 
		Py_DECREF(pyDbscan);
	}
}

argos::CColor CPFA_loop_functions::GetFloorColor(const argos::CVector2 &c_pos_on_floor) {
	return argos::CColor::WHITE;
}

void CPFA_loop_functions::UpdatePheromoneList() {
	// Return if this is not a tick that lands on a 0.5 second interval
	if ((int)(GetSpace().GetSimulationClock()) % ((int)(GetSimulator().GetPhysicsEngine("dyn2d").GetInverseSimulationClockTick()) / 2) != 0) return;
	
	std::vector<Pheromone> new_p_list; 

	argos::Real t = GetSpace().GetSimulationClock() / GetSimulator().GetPhysicsEngine("dyn2d").GetInverseSimulationClockTick();

	for(size_t i = 0; i < PheromoneList.size(); i++) {

		PheromoneList[i].Update(t);

		/**
		 * NOTE: 	Misleading trails that have captured robots will NEVER have an empty traveler list.
		 * 			When looping through PheromoneList in other functions, keep this in mind.
		 */

		if(!PheromoneList[i].IsActive() && PheromoneList[i].GetTravelerList().empty()) {
			/* Trails in the inativePheromoneList should only be those that have "evaporated" and have an empty traveler list. */
			inactivePheromoneList.push_back(PheromoneList[i]);
		} else {
			new_p_list.push_back(PheromoneList[i]);
		}
	}

	PheromoneList = new_p_list;
	new_p_list.clear();
}

// modified to include FakeFoodDistribution ** Ryan Luna 11/13/22
void CPFA_loop_functions::SetFoodDistribution() {

	if (UseAltDistribution){
		AlternateFakeFoodDistribution();
	} else if (UseFakeFoodDoS){
		switch(FoodDistribution) {
			case 0:
				RandomFoodDistribution();
				break;
			case 1:
				ClusterFoodDistribution();
				break;
			case 2:
				PowerLawFoodDistribution();
				break;
			default:
				argos::LOGERR << "ERROR: Invalid food distribution in XML file.\n";
		}
		switch(FakeFoodDistribution) {
			case 0:
				RandomFakeFoodDistribution();
				break;
			case 1:
				ClusterFakeFoodDistribution();
				break;
			case 2:
				PowerLawFakeFoodDistribution();
				break;
			default:
				argos::LOGERR << "ERROR: Invalid food distribution in XML file.\n";
		}
	} else if (UseFakeFoodOnly) {
		LOG << "[WARNING] This simulation is ONLY using Fake Food [WARNING] Real Food is NOT being distributed [WARNING]" << endl;
		switch(FakeFoodDistribution) {
			case 0:
				RandomFakeFoodDistribution();
				break;
			case 1:
				ClusterFakeFoodDistribution();
				break;
			case 2:
				PowerLawFakeFoodDistribution();
				break;
			default:
				argos::LOGERR << "ERROR: Invalid food distribution in XML file.\n";
		}
	} else {
		switch(FoodDistribution) {
			case 0:
				RandomFoodDistribution();
				break;
			case 1:
				ClusterFoodDistribution();
				break;
			case 2:
				PowerLawFoodDistribution();
				break;
			default:
				argos::LOGERR << "ERROR: Invalid food distribution in XML file.\n";
		}
	}
}

void CPFA_loop_functions::AlternateFakeFoodDistribution(){
	
	Real foodOffset;
	size_t foodPlaced = 0;
	if (densify){
		foodOffset = 2.0 * FoodRadius;
	} else {
		foodOffset = 3.0 * FoodRadius;
	}
	argos::CVector3 ArenaSize = GetSpace().GetArenaSize();
	float wallbuffer = 0.5;
	size_t ClusterLength = AltClusterLength;
	size_t ClusterWidth = AltClusterWidth;

	// West Wall
	CVector2 WestClusterPosition;
	size_t WestClusterX = ClusterLength;
	size_t WestClusterY = ClusterWidth;
	WestClusterPosition.Set(-ArenaSize.GetX()/2 + wallbuffer, foodOffset/2 + (((WestClusterY/2)-1) * foodOffset));
	
	for(size_t i = 0; i < WestClusterY; i++) {
		for(size_t j = 0; j < WestClusterX; j++) {
			foodPlaced++;

			Food tmp(WestClusterPosition, Food::FoodType::FAKE);
			FoodList.push_back(tmp);

			WestClusterPosition.SetX(WestClusterPosition.GetX() + foodOffset);
		}

		WestClusterPosition.SetX(WestClusterPosition.GetX() - (WestClusterX * foodOffset));
		WestClusterPosition.SetY(WestClusterPosition.GetY() - foodOffset);
	}

	// East Wall
	CVector2 EastClusterPosition;
	size_t EastClusterX = ClusterLength;
	size_t EastClusterY = ClusterWidth;
	EastClusterPosition.Set(ArenaSize.GetX()/2 - wallbuffer, foodOffset/2 + (((EastClusterY/2)-1) * foodOffset));
	
	for(size_t i = 0; i < EastClusterY; i++) {
		for(size_t j = 0; j < EastClusterX; j++) {
			foodPlaced++;

			Food tmp(EastClusterPosition, Food::FoodType::FAKE);
			FoodList.push_back(tmp);

			EastClusterPosition.SetX(EastClusterPosition.GetX() - foodOffset);
		}

		EastClusterPosition.SetX(EastClusterPosition.GetX() + (EastClusterX * foodOffset));
		EastClusterPosition.SetY(EastClusterPosition.GetY() - foodOffset);
	}

	// North Wall
	CVector2 NorthClusterPosition;
	size_t NorthClusterX = ClusterWidth;
	size_t NorthClusterY = ClusterLength;
	NorthClusterPosition.Set(foodOffset/2 + (((NorthClusterX/2)-1) * foodOffset), ArenaSize.GetY()/2 - wallbuffer);
	
	for(size_t i = 0; i < NorthClusterY; i++) {
		for(size_t j = 0; j < NorthClusterX; j++) {
			foodPlaced++;

			Food tmp(NorthClusterPosition, Food::FoodType::FAKE);
			FoodList.push_back(tmp);

			NorthClusterPosition.SetX(NorthClusterPosition.GetX() - foodOffset);
		}

		NorthClusterPosition.SetX(NorthClusterPosition.GetX() + (NorthClusterX * foodOffset));
		NorthClusterPosition.SetY(NorthClusterPosition.GetY() - foodOffset);
	}

	// South Wall
	CVector2 SouthClusterPosition;
	size_t SouthClusterX = ClusterWidth;
	size_t SouthClusterY = ClusterLength;
	SouthClusterPosition.Set(foodOffset/2 + (((SouthClusterX/2)-1) * foodOffset), -ArenaSize.GetY()/2 + wallbuffer);
	
	for(size_t i = 0; i < SouthClusterY; i++) {
		for(size_t j = 0; j < SouthClusterX; j++) {
			foodPlaced++;

			Food tmp(SouthClusterPosition, Food::FoodType::FAKE);
			FoodList.push_back(tmp);

			SouthClusterPosition.SetX(SouthClusterPosition.GetX() - foodOffset);
		}

		SouthClusterPosition.SetX(SouthClusterPosition.GetX() + (SouthClusterX * foodOffset));
		SouthClusterPosition.SetY(SouthClusterPosition.GetY() + foodOffset);
	}

}

void CPFA_loop_functions::DistributeAtkNests(){

	double L = static_cast<double>(ForagingAreaSize.GetX()); // Cast to double for division
	LOG << "Foraging Area Size = " << ForagingAreaSize.GetX() << "x" << ForagingAreaSize.GetY() << endl;

    // Define the bounds for the outer region of each primary quadrant
    // Assuming the center of the arena is (0,0) and the arena is a square
    double outer_bound = L / 2; // The outermost edge of the arena
    double inner_bound = L / 4; // The inner boundary for the outer region

    // Loop through each quadrant to place one attack nest
    for (size_t i = 0; i < 4; ++i) { // Ensure 4 nests
        double x_min, x_max, y_min, y_max;

        // Determine the bounds for the outer region of the current quadrant
        if (i == 0) { // Top Right Quadrant
            x_min = inner_bound + (AtkNestRadius + 0.1);
            x_max = outer_bound - (AtkNestRadius + 0.1);
            y_min = inner_bound + (AtkNestRadius + 0.1);
            y_max = outer_bound - (AtkNestRadius + 0.1);
        } else if (i == 1) { // Bottom Left Quadrant
            x_min = -outer_bound + (AtkNestRadius + 0.1);
            x_max = -inner_bound - (AtkNestRadius + 0.1);
            y_min = -outer_bound + (AtkNestRadius + 0.1);
            y_max = -inner_bound - (AtkNestRadius + 0.1);
        } else if (i == 2) { // Bottom Right Quadrant
            x_min = inner_bound + (AtkNestRadius + 0.1);
            x_max = outer_bound - (AtkNestRadius + 0.1);
            y_min = -outer_bound + (AtkNestRadius + 0.1);
            y_max = -inner_bound - (AtkNestRadius + 0.1);
        } else if (i == 3) { // Top Left Quadrant
            x_min = -outer_bound + (AtkNestRadius + 0.1);
            x_max = -inner_bound - (AtkNestRadius + 0.1);
            y_min = inner_bound + (AtkNestRadius + 0.1);
            y_max = outer_bound - (AtkNestRadius + 0.1);
        }

        // Generate random coordinates within the outer region of the selected quadrant
        argos::Real x = RNG->Uniform(CRange<argos::Real>(x_min, x_max));
        argos::Real y = RNG->Uniform(CRange<argos::Real>(y_min, y_max));

        // Create the nest position and add it to the list
        CVector2 nestPosition(x, y);
        AtkNestPositions.push_back(nestPosition);
    }

}

void CPFA_loop_functions::RandomFoodDistribution() {
	// FoodList.clear();
// 	FoodColoringList.clear();
	argos::CVector2 placementPosition;

	for(size_t i = 0; i < NumRealFood; i++) {
		placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

		while(IsOutOfBounds(placementPosition, 1, 1)) {
			placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));
		}

		Food tmp(placementPosition, Food::FoodType::REAL);
		FoodList.push_back(tmp);							// Ryan Luna 11/10/22
	}
}

// Ryan Luna 11/13/22
void CPFA_loop_functions::RandomFakeFoodDistribution(){

	CVector2 placementPosition;

	// distribute fake food 
	for(size_t i = 0; i < NumFakeFood; i++){
		placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

		while(IsOutOfBounds(placementPosition, 1, 1) || IsCollidingWithFood(placementPosition)) {
			placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));
		}

		Food tmp(placementPosition, Food::FoodType::FAKE);
		FoodList.push_back(tmp);
	}
}

void CPFA_loop_functions::ClusterFoodDistribution() {
    // FoodList.clear();
	argos::Real     foodOffset  = 3.0 * FoodRadius;
	size_t          foodToPlace = NumberOfClusters * ClusterWidthX * ClusterWidthY;
	size_t          foodPlaced = 0;
	argos::CVector2 placementPosition;

	NumRealFood = foodToPlace;

	for(size_t i = 0; i < NumberOfClusters; i++) {
		placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

		while(IsOutOfBounds(placementPosition, ClusterWidthY, ClusterWidthX)) {
			placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));
		}

		for(size_t j = 0; j < ClusterWidthY; j++) {
			for(size_t k = 0; k < ClusterWidthX; k++) {
				foodPlaced++;

				Food tmp(placementPosition, Food::FoodType::REAL);	// Ryan Luna 11/10/22
				FoodList.push_back(tmp);							// Ryan Luna 11/10/22

				placementPosition.SetX(placementPosition.GetX() + foodOffset);
			}

			placementPosition.SetX(placementPosition.GetX() - (ClusterWidthX * foodOffset));
			placementPosition.SetY(placementPosition.GetY() + foodOffset);
		}
	}
}

// Ryan Luna 11/13/22
void CPFA_loop_functions::ClusterFakeFoodDistribution(){
	
	size_t			fakefoodToPlace = NumFakeClusters * FakeClusterWidthX * FakeClusterWidthY;
	size_t			fakefoodPlaced = 0;
	CVector2		placementPosition;
	argos::Real		foodOffset;

	if (densify){
		foodOffset  = 2.0 * FoodRadius;
	} else {
		foodOffset  = 3.0 * FoodRadius;
	}

	NumFakeFood = fakefoodToPlace;

	for(size_t i = 0; i < NumFakeClusters; i++) {
		placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

		while(IsOutOfBounds(placementPosition, FakeClusterWidthY, FakeClusterWidthX)) {
			placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));
		}

		for(size_t j = 0; j < FakeClusterWidthY; j++) {
			for(size_t k = 0; k < FakeClusterWidthX; k++) {
				fakefoodPlaced++;

				Food tmp(placementPosition, Food::FoodType::FAKE);
				FoodList.push_back(tmp);

				placementPosition.SetX(placementPosition.GetX() + foodOffset);
			}

			placementPosition.SetX(placementPosition.GetX() - (FakeClusterWidthX * foodOffset));
			placementPosition.SetY(placementPosition.GetY() + foodOffset);
		}
	}
}

void CPFA_loop_functions::PowerLawFoodDistribution() {
 	// FoodList.clear();
	argos::Real foodOffset     = 3.0 * FoodRadius;
	size_t      foodPlaced     = 0;
	size_t      powerLawLength = 1;
	size_t      maxTrials      = 200;
	size_t      trialCount     = 0;

	std::vector<size_t> powerLawClusters;
	std::vector<size_t> clusterSides;
	argos::CVector2     placementPosition;

    //-----Wayne: Dertermine PowerRank and food per PowerRank group
    size_t priorPowerRank = 0;
    size_t power4 = 0;
    size_t FoodCount = 0;
    size_t diffFoodCount = 0;
    size_t singleClusterCount = 0;
    size_t otherClusterCount = 0;
    size_t modDiff = 0;

	// use local variable for power rank value not global ** Ryan Luna 11/13/22
	size_t localPowerRank = PowerRank;
    
    //Wayne: priorPowerRank is determined by what power of 4
    //plus a multiple of power4 increases the food count passed required count
    //this is how powerlaw works to divide up food into groups
    //the number of groups is the powerrank
    while (FoodCount < NumRealFood){
        priorPowerRank++;
        power4 = pow (4.0, priorPowerRank);
        FoodCount = power4 + priorPowerRank * power4;
    }
    
    //Wayne: Actual powerRank is prior + 1
    localPowerRank = priorPowerRank + 1;
    
    //Wayne: Equalizes out the amount of food in each group, with the 1 cluster group taking the
    //largest loss if not equal, when the powerrank is not a perfect fit with the amount of food.
    diffFoodCount = FoodCount - NumRealFood;
    modDiff = diffFoodCount % localPowerRank;
    
    if (NumRealFood % localPowerRank == 0){
        singleClusterCount = NumRealFood / localPowerRank;
        otherClusterCount = singleClusterCount;
    }
    else {
        otherClusterCount = NumRealFood / localPowerRank + 1;
        singleClusterCount = otherClusterCount - modDiff;
    }
    //-----Wayne: End of PowerRank and food per PowerRank group
    
	for(size_t i = 0; i < localPowerRank; i++) {
		powerLawClusters.push_back(powerLawLength * powerLawLength);
		powerLawLength *= 2;
	}

	for(size_t i = 0; i < localPowerRank; i++) {
		powerLawLength /= 2;
		clusterSides.push_back(powerLawLength);
	}
    /*Wayne: Modified to break from loops if food count reached.
     Provides support for unequal clusters and odd food numbers.
     Necessary for DustUp and Jumble Distribution changes. */
    
	for(size_t h = 0; h < powerLawClusters.size(); h++) {
		for(size_t i = 0; i < powerLawClusters[h]; i++) {
			placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

			while(IsOutOfBounds(placementPosition, clusterSides[h], clusterSides[h])) {
				trialCount++;
				placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

				if(trialCount > maxTrials) {
					argos::LOGERR << "PowerLawDistribution(): Max trials exceeded!\n";
					break;
				}
			}

            trialCount = 0;
			for(size_t j = 0; j < clusterSides[h]; j++) {
				for(size_t k = 0; k < clusterSides[h]; k++) {
					foodPlaced++;
					// FoodList.push_back(placementPosition);
					// FoodColoringList.push_back(argos::CColor::BLACK);

					Food tmp(placementPosition, Food::FoodType::REAL);
					FoodList.push_back(tmp);							// Ryan Luna 11/10/22
					placementPosition.SetX(placementPosition.GetX() + foodOffset);
                    if (foodPlaced == singleClusterCount + h * otherClusterCount) break;
				}

				placementPosition.SetX(placementPosition.GetX() - (clusterSides[h] * foodOffset));
				placementPosition.SetY(placementPosition.GetY() + foodOffset);
                if (foodPlaced == singleClusterCount + h * otherClusterCount) break;
			}
            if (foodPlaced == singleClusterCount + h * otherClusterCount) break;
			}
		}
	NumRealFood = foodPlaced;
}

void CPFA_loop_functions::PowerLawFakeFoodDistribution() {

	// variable name modification 'L_' to denote a local function variable ** Ryan Luna 11/13/22

	argos::Real L_foodOffset     = 3.0 * FoodRadius;
	size_t      L_fakefoodPlaced     = 0;
	size_t      L_powerLawLength = 1;
	size_t      L_maxTrials      = 200;
	size_t      L_trialCount     = 0;

	std::vector<size_t> L_powerLawFakeClusters;
	std::vector<size_t> L_fakeClusterSides;
	argos::CVector2     L_placementPosition;

    //-----Wayne: Dertermine PowerRank and food per PowerRank group
    size_t L_priorPowerRank = 0;
    size_t L_power4 = 0;
    size_t L_FakeFoodCount = 0;
    size_t L_diffFakeFoodCount = 0;
    size_t L_singleFakeClusterCount = 0;
    size_t L_otherFakeClusterCount = 0;
    size_t L_modDiff = 0;

	size_t localPowerRank = PowerRank;
    
    //Wayne: L_priorPowerRank is determined by what power of 4
    //plus a multiple of L_power4 increases the food count passed required count
    //this is how powerlaw works to divide up food into groups
    //the number of groups is the powerrank
    while (L_FakeFoodCount < NumFakeFood){
        L_priorPowerRank++;
        L_power4 = pow (4.0, L_priorPowerRank);
        L_FakeFoodCount = L_power4 + L_priorPowerRank * L_power4;
    }
    
    //Wayne: Actual powerRank is prior + 1
    localPowerRank = L_priorPowerRank + 1;
    
    //Wayne: Equalizes out the amount of food in each group, with the 1 cluster group taking the
    //largest loss if not equal, when the powerrank is not a perfect fit with the amount of food.
    L_diffFakeFoodCount = L_FakeFoodCount - NumFakeFood;
    L_modDiff = L_diffFakeFoodCount % localPowerRank;
    
    if (NumFakeFood % localPowerRank == 0){
        L_singleFakeClusterCount = NumFakeFood / localPowerRank;
        L_otherFakeClusterCount = L_singleFakeClusterCount;
    }
    else {
        L_otherFakeClusterCount = NumFakeFood / localPowerRank + 1;
        L_singleFakeClusterCount = L_otherFakeClusterCount - L_modDiff;
    }
    //-----Wayne: End of PowerRank and food per PowerRank group
    
	for(size_t i = 0; i < localPowerRank; i++) {
		L_powerLawFakeClusters.push_back(L_powerLawLength * L_powerLawLength);
		L_powerLawLength *= 2;
	}

	for(size_t i = 0; i < localPowerRank; i++) {
		L_powerLawLength /= 2;
		L_fakeClusterSides.push_back(L_powerLawLength);
	}
    /*Wayne: Modified to break from loops if food count reached.
     Provides support for unequal clusters and odd food numbers.
     Necessary for DustUp and Jumble Distribution changes. */
    
	for(size_t h = 0; h < L_powerLawFakeClusters.size(); h++) {
		for(size_t i = 0; i < L_powerLawFakeClusters[h]; i++) {
			L_placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

			while(IsOutOfBounds(L_placementPosition, L_fakeClusterSides[h], L_fakeClusterSides[h])) {
				L_trialCount++;
				L_placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

				if(L_trialCount > L_maxTrials) {
					argos::LOGERR << "PowerLawDistribution(): Max trials exceeded!\n";
					break;
				}
			}

            L_trialCount = 0;
			for(size_t j = 0; j < L_fakeClusterSides[h]; j++) {
				for(size_t k = 0; k < L_fakeClusterSides[h]; k++) {
					L_fakefoodPlaced++;
					// FoodList.push_back(L_placementPosition);
					// FoodColoringList.push_back(argos::CColor::BLACK);

					Food tmp(L_placementPosition, Food::FoodType::FAKE);
					FoodList.push_back(tmp);							
					L_placementPosition.SetX(L_placementPosition.GetX() + L_foodOffset);
                    if (L_fakefoodPlaced == L_singleFakeClusterCount + h * L_otherFakeClusterCount) break;
				}

				L_placementPosition.SetX(L_placementPosition.GetX() - (L_fakeClusterSides[h] * L_foodOffset));
				L_placementPosition.SetY(L_placementPosition.GetY() + L_foodOffset);
                if (L_fakefoodPlaced == L_singleFakeClusterCount + h * L_otherFakeClusterCount) break;
			}
            if (L_fakefoodPlaced == L_singleFakeClusterCount + h * L_otherFakeClusterCount) break;
			}
		}
	NumFakeFood = L_fakefoodPlaced;
}

bool CPFA_loop_functions::IsOutOfBounds(argos::CVector2 p, size_t length, size_t width) {
	argos::CVector2 placementPosition = p;

	argos::Real foodOffset   = 3.0 * FoodRadius;
	argos::Real widthOffset  = 3.0 * FoodRadius * (argos::Real)width;
	argos::Real lengthOffset = 3.0 * FoodRadius * (argos::Real)length;

	argos::Real x_min = p.GetX() - FoodRadius;
	argos::Real x_max = p.GetX() + FoodRadius + widthOffset;

	argos::Real y_min = p.GetY() - FoodRadius;
	argos::Real y_max = p.GetY() + FoodRadius + lengthOffset;

	if(		(x_min < (ForageRangeX.GetMin() + FoodRadius)) ||
			(x_max > (ForageRangeX.GetMax() - FoodRadius)) ||
			(y_min < (ForageRangeY.GetMin() + FoodRadius)) ||
			(y_max > (ForageRangeY.GetMax() - FoodRadius)))
	{
		return true;
	}

	for(size_t j = 0; j < length; j++) {
		for(size_t k = 0; k < width; k++) {
			if(IsCollidingWithFood(placementPosition)) return true;
			if(IsCollidingWithNest(placementPosition)) return true;
			if(IsCollidingWithAtkNest(placementPosition)) return true;
			placementPosition.SetX(placementPosition.GetX() + foodOffset);
		}

		placementPosition.SetX(placementPosition.GetX() - (width * foodOffset));
		placementPosition.SetY(placementPosition.GetY() + foodOffset);
	}

	return false;
}

bool CPFA_loop_functions::IsCollidingWithNest(argos::CVector2 p) {
	argos::Real nestRadiusPlusBuffer = NestRadius + FoodRadius;
	argos::Real NRPB_squared = nestRadiusPlusBuffer * nestRadiusPlusBuffer;

      return ( (p - NestPosition).SquareLength() < NRPB_squared ) ;
}

bool CPFA_loop_functions::IsCollidingWithAtkNest(argos::CVector2 p) {
	argos::Real nestRadiusPlusBuffer = AtkNestRadius + FoodRadius;
	argos::Real NRPB_squared = nestRadiusPlusBuffer * nestRadiusPlusBuffer;

    //   return ( 	(p - AtkNest1Position).SquareLength() < NRPB_squared ||
	//   			(p - AtkNest2Position).SquareLength() < NRPB_squared ||
	// 			(p - AtkNest3Position).SquareLength() < NRPB_squared ||
	// 			(p - AtkNest4Position).SquareLength() < NRPB_squared	);

	for (size_t i = 0; i < AtkNestPositions.size(); ++i) {
		if ((p - AtkNestPositions[i]).SquareLength() < NRPB_squared) {
			return true;
		}
	}
	return false;
}

bool CPFA_loop_functions::IsCollidingWithFood(argos::CVector2 p) {
	argos::Real foodRadiusPlusBuffer = 2.0 * FoodRadius;
	argos::Real FRPB_squared = foodRadiusPlusBuffer * foodRadiusPlusBuffer;

	for(size_t i = 0; i < FoodList.size(); i++) {
		if((p - FoodList[i].GetLocation()).SquareLength() < FRPB_squared) return true;
	}

	return false;
}

unsigned int CPFA_loop_functions::getNumberOfRobots() {
	return GetSpace().GetEntitiesByType("foot-bot").size();
}

double CPFA_loop_functions::getProbabilityOfSwitchingToSearching() {
	return ProbabilityOfSwitchingToSearching;
}

double CPFA_loop_functions::getProbabilityOfReturningToNest() {
	return ProbabilityOfReturningToNest;
}

// Value in Radians
double CPFA_loop_functions::getUninformedSearchVariation() {
	return UninformedSearchVariation.GetValue();
}

double CPFA_loop_functions::getRateOfInformedSearchDecay() {
	return RateOfInformedSearchDecay;
}

double CPFA_loop_functions::getRateOfSiteFidelity() {
	return RateOfSiteFidelity;
}

double CPFA_loop_functions::getRateOfLayingPheromone() {
	return RateOfLayingForagerPheromone;
}

double CPFA_loop_functions::getRateOfPheromoneDecay() {
	return RateOfPheromoneDecay;
}

argos::Real CPFA_loop_functions::getSimTimeInSeconds() {
	int ticks_per_second = GetSimulator().GetPhysicsEngine("dyn2d").GetInverseSimulationClockTick(); //qilu 02/06/2021
	float sim_time = GetSpace().GetSimulationClock();
	return sim_time/ticks_per_second;
}

void CPFA_loop_functions::SetTrial(unsigned int v) {
}

void CPFA_loop_functions::setScore(double s) {
	score = s;
    
	// if (score >= NumDistributedRealFood) {
	// 	PostExperiment();
	// }
}

double CPFA_loop_functions::Score() {	
	return score;
}

// modified ** Ryan Luna 11/12/22
void CPFA_loop_functions::increaseNumDistributedFoodByOne(){
    NumDistributedRealFood++;
	TotalDistributedFood++;
}

void CPFA_loop_functions::ConfigureFromGenome(Real* g)
{
	// Assign genome generated by the GA to the appropriate internal variables.
	ProbabilityOfSwitchingToSearching = g[0];
	ProbabilityOfReturningToNest      = g[1];
	UninformedSearchVariation.SetValue(g[2]);
	RateOfInformedSearchDecay         = g[3];
	RateOfSiteFidelity                = g[4];
	RateOfLayingForagerPheromone             = g[5];
	RateOfPheromoneDecay              = g[6];
}

void CPFA_loop_functions::CaptureRobotInAtkNest(string robot_id){
	AttackerNest.CaptureRobot(robot_id);

	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");

	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		// BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
		if (footBot.GetId() == robot_id){
			BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
			if (c != nullptr){
				CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
				if (c2 != nullptr){

					CEmbodiedEntity& cEmbodiedEntity = footBot.GetEmbodiedEntity();
					
					try {

						CVector3 newPosition = GenCapturePosition();
						argos::CVector3& curPosition = footBot.GetEmbodiedEntity().GetOriginAnchor().Position;
						size_t tryCount = 0;
						const size_t tryLimit = 10;
						const Real positionThreshold = 0.001; 	// Threshold for considering positions as equal 
																// (for precision errors when comparing floating point numbers)

						/**
						 * GPT: The multiplication of positionThreshold with itself
						 * is done to compare the squared distance between the new position and the 
						 * current position against the squared threshold.
						 */
    					while ((newPosition - curPosition).SquareLength() > positionThreshold * positionThreshold) {

							newPosition = GenCapturePosition();

							// if (robot_id == "fb22") {
							// 	LOG << "fb22: " << newPosition << endl;
							// }
							
							// Attempt to move the entity
							MoveEntity(
								cEmbodiedEntity,
								newPosition,          			// New position
								argos::CQuaternion()          	// New orientation (identity quaternion means no rotation)
							);

							curPosition = footBot.GetEmbodiedEntity().GetOriginAnchor().Position;

							// if (newPosition == curPosition) break;		// We can just exit here once these values match

							if (tryCount > tryLimit){
								LOGERR << "ERROR: Failed to move entity " << footBot.GetId() << endl;
								Terminate();
								break;
							}

							tryCount++;
						}
						
					} catch (const argos::CARGoSException& ex) {
						// Log the exception details
						LOGERR << "Exception when moving entity: " << ex.what() << endl;
					} catch (std::exception& ex) {
						// Catch any other exceptions that might be thrown
						LOGERR << "Standard exception when moving entity: " << ex.what() << endl;
					} catch (...) {
						// Catch any other non-standard exceptions
						LOGERR << "An unknown exception occurred when moving entity" << endl;
					}

					c2->SetAsCaptured();

					// LOG << footBot.GetId() << ": Captured and moved." << endl;

				} else {
					LOG << "CPFA_controller cast failed." << endl;
				}
			} else {
				LOG << "BaseController cast failed." << endl;
			}
		}
	}

}

CVector3 CPFA_loop_functions::GenCapturePosition(){
	argos::CVector2 placementPosition;


    // Define the holding area ranges
    argos::CRange<argos::Real> HoldingRangeX(5.15, 5.85);
    argos::CRange<argos::Real> HoldingRangeY(-4.85, 4.85);

	// Generate a random placement within the holding area
	placementPosition.Set(RNG->Uniform(HoldingRangeX), RNG->Uniform(HoldingRangeY));

	// make sure it isn't colliding with anything (like another robot)
	while(IsNearRobot(placementPosition)) {
		placementPosition.Set(RNG->Uniform(HoldingRangeX), RNG->Uniform(HoldingRangeY));
	}

	// LOG << "PlacementPosition: " << CVector3(placementPosition.GetX(), placementPosition.GetY(), 0.0) << endl;
	return CVector3(placementPosition.GetX(), placementPosition.GetY(), 0.0);
}

bool CPFA_loop_functions::IsNearRobot(const argos::CVector2& position) {
	const Real footBotRadius = 0.085;
	const Real buf = 0.01;
	const Real minDistance = footBotRadius + buf;
	
    // Loop through all robots and check their positions
	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");
	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
		CVector2 robotPosition = c->GetPosition();
		// Real d = sqrt( pow( abs(position.GetX()) - abs(robotPosition.GetX()), 2) + pow( abs(position.GetY()) - abs(robotPosition.GetY()), 2) );
		Real d = sqrt( pow(position.GetX() - robotPosition.GetX(), 2) + pow(position.GetY() - robotPosition.GetY(), 2) );

        if(d < minDistance) {
			// LOG << "Too close to robot " << footBot.GetId() << endl;
            return true; // Too close to a robot
        }
	}

    return false; // Not close to any robot
}

CVector2 CPFA_loop_functions::GetNestLocation(){
	return NestPosition;
}

// Real CPFA_loop_functions::GetBotFwdSpeed(){
// 	return BotFwdSpeed;
// }

void CPFA_loop_functions::PushToTrailLog(std::string bot_id, Pheromone P, Real startTime){
	trailLog.push_back(make_tuple(bot_id, P, startTime, false));
}

void CPFA_loop_functions::PopFromTrailLog(std::string bot_id){
	for (size_t i = 0; i < trailLog.size(); i++){
		if (get<0>(trailLog[i]) == bot_id){

			trailLog.erase(trailLog.begin() + i);

			for (size_t j = 0; j < PheromoneList.size(); j++){

				if (PheromoneList[j].GetLocation() == get<1>(trailLog[i]).GetLocation()){

					if (PheromoneList[j].GetCreatorId() == bot_id){

						PheromoneList[j].SetReturned(true);		// log that a bot has returned to the nest after using this trail

						if (PheromoneList[j].IsMisleading() && bot_id.find("fb") != string::npos){
							
							LOGERR << "ERROR: "<< bot_id << " returned from \"Misleading Trail\" at location " << PheromoneList[j].GetLocation() << endl;
						}
						break;
					}
					
				}
			}
		}
	}
}

Pheromone& CPFA_loop_functions::GetTrailFollowed(std::string bot_id){
	for (size_t i = 0; i < PheromoneList.size(); i++){
		for (size_t j = 0; j < PheromoneList[i].GetTravelerList().size(); j++){
			if (PheromoneList[i].GetTravelerList()[j].first == bot_id){
				return PheromoneList[i];
			}
		}
	}
	LOGERR << "ERROR: In GetTrailFollowed(): No trail found for " << bot_id << "in PheromoneList." << endl;
	LOGERR << "In GetTrailFollowed(): Searching in inactivePheromoneList..." << endl;
	for (size_t i = 0; i < inactivePheromoneList.size(); i++){
		for (size_t j = 0; j < inactivePheromoneList[i].GetTravelerList().size(); j++){
			if (inactivePheromoneList[i].GetTravelerList()[j].first == bot_id){
				LOGERR << "In GetTrailFollowed(): Trail found for " << bot_id << "in inactivePheromoneList." << endl;
			}
		}
	}
	LOGERR << "ERROR: In GetTrailFollowed(): No trail found for " << bot_id << "in inactivePheromoneList." << endl;
	Terminate();
	throw "ERROR: In GetTrailFollowed(): No trail found for " + bot_id;
}

vector<CVector3> CPFA_loop_functions::GetAtkNestList(){
	vector<CVector3> AtkNestList3d;
	for (CVector2 atkNestPos : AtkNestPositions){
		AtkNestList3d.push_back(CVector3(atkNestPos.GetX(), atkNestPos.GetY(), 0.0));
	}
	return AtkNestList3d;
}

Real CPFA_loop_functions::T_estimate(Real d, Real v){
	if (useFeedbackEq)
		return (d / v) * k;
	else
		// LOG << "uniVelocity: " << uniVelocity << endl;
		return (d / uniVelocity);
}

void CPFA_loop_functions::LogReturn(std::string bot_id, Real returnTime, bool returnedFromTrail){

	bool found = false; // this is for error checking

	// LOG << "LogReturn called ... " << endl;

	// for (auto& b_name : tmpNameStorage){
	// 	if (b_name == bot_id){
	// 		LOGERR << bot_id << " has returned..." << endl;
	// 	}
	// }

	// if (bot_id == "fb22") LOG << "fb22 has returned..." << endl;
	// loop through the traveler lists of each pheromone object looking for the bot_id (there should only be one)
	for (size_t i = 0; i < PheromoneList.size(); i++){
		
		vector<pair<string, Real>> traveler = PheromoneList[i].GetTravelerList();
		
		for (size_t j = 0; j < traveler.size(); j++){

			if (traveler[j].first == bot_id && !found){

				// for (auto& b_name : tmpNameStorage){
				// 	if (b_name == bot_id){
				// 		LOGERR << bot_id << " found in traveler list of PheromoneList[" << i << "]" << endl;
				// 	}
				// }

				// if (bot_id == "fb22") LOG << bot_id << " found in traveler list of PheromoneList[" << i << "]" << endl;

				found = true;

				if (!PheromoneList[i].HasReturnedARobot() && returnedFromTrail) PheromoneList[i].SetReturned(true);

				/* UPDATE 'k' FOR TRAVEL TIME ESTIMATE */

				// Get travel time estimate
				CVector2 trailPos = PheromoneList[i].GetLocation();
				Real trailLength = sqrt( pow(NestPosition.GetX() - trailPos.GetX(), 2) + pow(NestPosition.GetY() - trailPos.GetY(), 2) );
				Real d = trailLength * 2;	// multiply by 2 to get distance to and from the target location
				Real v = BotFwdSpeed;	
				// LOG << "v: " << v << endl;

				// get recorded travel time (return_time - start_time)
				Real T_actual = returnTime - traveler[j].second;

				/**
				 * NOTE: 	I am choosing not to add the tolerance to the travel time estimate here. This is
				 * 			so that even if the actual travel time is only slightly greater than the estimate, 
				 * 			it doesn't get flagged but we still update for better accuracy
				 */

				// LOG << "T_actual: " << T_actual << endl;
				// LOG << "T_estimate: " << T_estimate(d,v) << endl;
				if (T_actual > T_estimate(d,v)){

					// if (bot_id == "fb22") LOG << "T_actual > T_estimate(d,v)" << endl;

					// LOG << "Travel time estimate exceed upon return..." << endl;

					if (useFeedbackEq){
						Real epsilon = T_actual - T_estimate(d,v);

						// update correction variable 'k'
						k = k * (1 + alpha * (epsilon/T_actual));
					} else {
						// update unified velocity
						uniVelocity = d / T_actual;
						// LOG << "travel time estimate updated (uniVelocity): " << uniVelocity << endl;
					}

					// update estimate travel time in pheromone object (not sure if this is still necessary as it isn't used anywhere yet)
					PheromoneList[i].SetEstTravelTime(T_estimate(d,v));

				}
				if (!useClustering){
					/**
					 * When a robot who's exceeded the estimted travel time returns, we must remove a strike against the creator of the trail.
					 */

					if (isolatedBots.find(PheromoneList[i].GetCreatorId()) != isolatedBots.end()){

						// remove bot from isolation
						UnIsolateBot(PheromoneList[i].GetCreatorId());

					} 
					
					if (strikeMap[PheromoneList[i].GetCreatorId()].find(bot_id) != strikeMap[PheromoneList[i].GetCreatorId()].end()){

						strikeMap[PheromoneList[i].GetCreatorId()].erase(bot_id);

						if (strikeMap[PheromoneList[i].GetCreatorId()].size() == 0){

							strikeMap.erase(PheromoneList[i].GetCreatorId());
						}

						// a detractor had a strike removed (add to false negatives)
						if (PheromoneList[i].GetCreatorId().find("dt") != string::npos){
							falseNegatives++;
						}
					}

				/******************************************** CLUSTER & CLUSTER GRAPH DEFENSE *******************************************************/
				} else {

					// Variables to hold cluster data
					int clusterLabel = -1;
					std::unordered_set<std::string> creatorsToProcess;
					clusterLabel = clusterLabels[i]; // clusterLabels[i] should be the cluster label for the trail at index i
					// if (bot_id == "fb22") LOG << "In LogReturn(): setting up creatorsToProcess, Cluster Label: " <<  clusterLabel << endl;

					// if clustering only
					if (useClustering && !useClusterGraph) {

						if (clusterLabel == -1){
							string creator = PheromoneList[i].GetCreatorId();
							creatorsToProcess.insert(creator);
						} else {
							for (int trailIndex : clusterMembers[clusterLabel]) {
								string creator = PheromoneList[trailIndex].GetCreatorId();
								creatorsToProcess.insert(creator);
							}
						}

					// if cluster graph
					} else if (useClustering && useClusterGraph) {

						int nodeId; // Identifier for the node in the graph

						if (clusterLabel == -1){

							// The trail is a noise point, find its unique identifier
							auto noisePointIt = std::find(nonClusteredPoints.begin(), nonClusteredPoints.end(), i);

							if (noisePointIt != nonClusteredPoints.end()) {

								int noisePointIndex = std::distance(nonClusteredPoints.begin(), noisePointIt);
								nodeId = -(noisePointIndex + 1);
							}

						} else nodeId = clusterLabel;
						// int nodeId = (clusterLabel != -1) ? clusterLabel : GetNoisePointIdentifier(i, nonClusteredPoints);
						
						std::set<int> neighbors = GetNeighbors(nodeId);
						for (int neighborId : neighbors) {
							for (int trailIndex : clusterMembers[neighborId]) {
								string creator = PheromoneList[trailIndex].GetCreatorId();
								creatorsToProcess.insert(creator);
							}
						}
					}

					// if (tmpNameStorage.find(bot_id) != tmpNameStorage.end()){
					// 	for (const auto& creator : creatorsToProcess){
					// 		LOG << "bot_id: " << bot_id << endl;
					// 		LOG << "In LogReturn(): creatorsToProcess.size() = " << creatorsToProcess.size() << endl;
					// 		LOG << "In LogReturn(): creatorsToProcess: " << creator << endl;
					// 	}
					// } else {
					// 	// LOG << bot_id << ": test" << endl;
					// }

					if (bot_id == "fb22" && creatorsToProcess.size() > 0){
						
						// LOG << "In LogReturn(): " << endl;

						for (const auto& creator : creatorsToProcess){
							// LOG << "In LogReturn(): creatorsToProcess.size() = " << creatorsToProcess.size() << endl;
							// LOG << "In LogReturn(): creator in creatorsToProcess: " << creator << endl;
						}
					} else {
						// LOG << "fb22 creatorsToProcess.size() = " << creatorsToProcess.size() << endl;
					}
					

					// Remove the bot_id from the strikeMap for each creator in the creatorsToProcess set
					for (const auto& creator : creatorsToProcess) {
						if (strikeMap.find(creator) != strikeMap.end()) {
							// if (creator == "fb13" && bot_id == "fb22") LOGERR << "In LogReturn(): fb22 found fb13 in strikeMap" << endl;
							strikeMap[creator].erase(bot_id);
							if (strikeMap[creator].empty()) {
								strikeMap.erase(creator);
							}
						} else if (isolatedBots.find(creator) != isolatedBots.end()) {
							UnIsolateBot(creator);
							isolatedBots.erase(creator);
						} else {
							// LOG << "In LogReturn(): isolatedBots.size() = " << isolatedBots.size() << endl;
						}
					}
				}


					// TODO: If we unisolate robots in connected clusters if a robot returns on a trail in one of the connected clusters, 
					//			we risk unisolating all detractors if they are all connected. Should we isolate only the creator of the trail 
					//			that the robot returned on?

				PheromoneList[i].RemoveTraveler(bot_id);

			// We continue to loop through the pheromone traveler lists to check if the bot_id is in any other traveler lists. ** This should not happen **
			} else if (traveler[j].first == bot_id && found){
				LOGERR << "ERROR: Multiple instances of " << bot_id << " found in traveler list of pheromone object at location " << PheromoneList[i].GetLocation() << endl;
				Terminate();
			}
		}
	}

	// The bot_id should be in one of the traveler lists, if not, throw an error (This indicates that there is something wrong with the logic in the controller code)
	if (!found){
		bool found2 = false;
		LOGERR << "ERROR: In LogReturn(): No trail found for " << bot_id << endl;
		LOGERR << "In LogReturn(): Searching in inactivePheromoneList..." << endl;
		for (size_t i = 0; i < inactivePheromoneList.size(); i++){
			for (size_t j = 0; j < inactivePheromoneList[i].GetTravelerList().size(); j++){
				if (inactivePheromoneList[i].GetTravelerList()[j].first == bot_id){
					LOGERR << "In LogReturn(): Trail found for " << bot_id << " in inactivePheromoneList." << endl;
					found2 = true;
				}
			}
		}
		if (!found2) LOGERR << "ERROR: In LogReturn(): No trail found for " << bot_id << " in inactivePheromoneList." << endl;
		Terminate();
	} else {
		// LOG << bot_id << " return logged successfully..." << endl;
	}
}

void CPFA_loop_functions::IsolateBot(std::string bot_id){

	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");

	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		// BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
		if (footBot.GetId() == bot_id){
			BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
			if (c != nullptr){
				CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
				if (c2 != nullptr){

					CEmbodiedEntity& cEmbodiedEntity = footBot.GetEmbodiedEntity();
					
					try {

						CVector3 newPosition = GenIsoPosition();
						argos::CVector3& curPosition = footBot.GetEmbodiedEntity().GetOriginAnchor().Position;
						size_t tryCount = 0;
						const size_t tryLimit = 10;
						const Real positionThreshold = 0.001; 	// Threshold for considering positions as equal 
																// (for precision errors when comparing floating point numbers)

						/**
						 * GPT: The multiplication of positionThreshold with itself
						 * is done to compare the squared distance between the new position and the 
						 * current position against the squared threshold.
						 */
    					while ((newPosition - curPosition).SquareLength() > positionThreshold * positionThreshold) {

							newPosition = GenIsoPosition();

							// if (bot_id == "fb22") {
							// 	LOG << "fb22: " << newPosition << endl;
							// }
							
							// Attempt to move the entity
							MoveEntity(
								cEmbodiedEntity,
								newPosition,          			// New position
								argos::CQuaternion()          	// New orientation (identity quaternion means no rotation)
							);

							curPosition = footBot.GetEmbodiedEntity().GetOriginAnchor().Position;

							// if (newPosition == curPosition) break;		// We can just exit here once these values match

							if (tryCount > tryLimit){
								LOGERR << "ERROR: Failed to move entity " << footBot.GetId() << endl;
								Terminate();
								break;
							}

							tryCount++;
						}
						
					} catch (const argos::CARGoSException& ex) {
						// Log the exception details
						LOGERR << "Exception when moving entity: " << ex.what() << endl;
					} catch (std::exception& ex) {
						// Catch any other exceptions that might be thrown
						LOGERR << "Standard exception when moving entity: " << ex.what() << endl;
					} catch (...) {
						// Catch any other non-standard exceptions
						LOGERR << "An unknown exception occurred when moving entity" << endl;
					}

					c2->SetAsIsolated();

					LOG << footBot.GetId() << ": Isolated and moved." << endl;
					if (footBot.GetId().find("fb") != string::npos){
						IsoFalsePositives++;
					}
					numIsolatedBots++;

				} else {
					LOG << "CPFA_controller cast failed." << endl;
				}
			} else {
				LOG << "BaseController cast failed." << endl;
			}
		}
	}
}

void CPFA_loop_functions::UnIsolateBot(std::string bot_id){
	// loop through bots
	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");
	for(argos::CSpace::TMapPerType::iterator it = footbots.begin(); it != footbots.end(); it++) {
		argos::CFootBotEntity& footBot = *argos::any_cast<argos::CFootBotEntity*>(it->second);
		// BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
		if (footBot.GetId() == bot_id){
			BaseController* c = dynamic_cast<BaseController*>(&footBot.GetControllableEntity().GetController());
			if (c != nullptr){
				CPFA_controller* c2 = dynamic_cast<CPFA_controller*>(c);
				if (c2 != nullptr){

					CEmbodiedEntity& cEmbodiedEntity = footBot.GetEmbodiedEntity();
					
					try {

						CVector3 newPosition = GenUnIsoPosition();
						argos::CVector3& curPosition = footBot.GetEmbodiedEntity().GetOriginAnchor().Position;
						size_t tryCount = 0;
						const size_t tryLimit = 10;
						const Real positionThreshold = 0.001; 	// Threshold for considering positions as equal 
																// (for precision errors when comparing floating point numbers)

						/**
						 * GPT: The multiplication of positionThreshold with itself
						 * is done to compare the squared distance between the new position and the 
						 * current position against the squared threshold.
						 */
						while ((newPosition - curPosition).SquareLength() > positionThreshold * positionThreshold) {

							newPosition = GenUnIsoPosition();

							// if (bot_id == "fb22") {
							// 	LOG << "fb22: " << newPosition << endl;
							// }
							
							// Attempt to move the entity
							MoveEntity(
								cEmbodiedEntity,
								newPosition,          			// New position
								argos::CQuaternion()          	// New orientation (identity quaternion means no rotation)
							);

							curPosition = footBot.GetEmbodiedEntity().GetOriginAnchor().Position;

							// if (newPosition == curPosition) break;		// We can just exit here once these values match

							if (tryCount > tryLimit){
								LOGERR << "ERROR: Failed to move entity (unisolation)" << footBot.GetId() << endl;
								Terminate();
								break;
							}
						}

						} catch (const argos::CARGoSException& ex) {
						// Log the exception details
						LOGERR << "Exception when moving entity: " << ex.what() << endl;
					} catch (std::exception& ex) {
						// Catch any other exceptions that might be thrown
						LOGERR << "Standard exception when moving entity: " << ex.what() << endl;
					} catch (...) {
						// Catch any other non-standard exceptions
						LOGERR << "An unknown exception occurred when moving entity" << endl;
					}

					c2->SetUnIsolated();

					LOG << footBot.GetId() << ": Unisolated and returned to arena." << endl;
					if (footBot.GetId().find("dt") != string::npos){
						UnIsoFalsePositives++;
					}
					numUnIsolatedBots++;

				} else {
					LOG << "CPFA_controller cast failed." << endl;
				}
			} else {
				LOG << "BaseController cast failed." << endl;
			}
		}
	}
}

CVector3 CPFA_loop_functions::GenUnIsoPosition(){
	argos::CVector2 placementPosition;

	// Generate a random placement within the holding area
	placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));

	// make sure it isn't colliding with anything (like another robot)
	while(IsNearRobot(placementPosition)) {
		placementPosition.Set(RNG->Uniform(ForageRangeX), RNG->Uniform(ForageRangeY));
	}

	// LOG << "PlacementPosition: " << CVector3(placementPosition.GetX(), placementPosition.GetY(), 0.0) << endl;
	return CVector3(placementPosition.GetX(), placementPosition.GetY(), 0.0);
}

CVector3 CPFA_loop_functions::GenIsoPosition(){
	argos::CVector2 placementPosition;

    // Define the holding area ranges
    argos::CRange<argos::Real> HoldingRangeX(-5.85, -5.15);
    argos::CRange<argos::Real> HoldingRangeY(-4.85, 4.85);

	// Generate a random placement within the holding area
	placementPosition.Set(RNG->Uniform(HoldingRangeX), RNG->Uniform(HoldingRangeY));

	// make sure it isn't colliding with anything (like another robot)
	while(IsNearRobot(placementPosition)) {
		placementPosition.Set(RNG->Uniform(HoldingRangeX), RNG->Uniform(HoldingRangeY));
	}

	// LOG << "PlacementPosition: " << CVector3(placementPosition.GetX(), placementPosition.GetY(), 0.0) << endl;
	return CVector3(placementPosition.GetX(), placementPosition.GetY(), 0.0);
}

bool CPFA_loop_functions::SetupPythonEnvironment(){

	Py_Initialize();
	if(Py_IsInitialized()){
		LOG << "Python version: " << Py_GetVersion() << endl;
	} else {
		LOGERR << "ERROR: Python failed to initialize." << endl;
		return 0;	
	}

	
	PyObject *sys = PyImport_ImportModule("sys");
	PyObject *path = PyObject_GetAttrString(sys, "path");
	PyList_Append(path, PyUnicode_FromString("/home/Ryan/Foraging_Swarm_Defense/CPFA/source/CPFA"));
	PyObject *repr = PyObject_Repr(path);
	const char* s = PyUnicode_AsUTF8(repr);
	// LOG << "Python path: " << s << endl;
	Py_DECREF(repr);
	Py_DECREF(path);
	Py_DECREF(sys);

	// Load the module
	pyFileName = PyUnicode_FromString("dbscan");
	if (pyFileName == NULL) {
		LOG << "Error converting module name to PyUnicode" << std::endl;
		Py_Finalize();
		return 0;
	}

	pyModule = PyImport_Import(pyFileName);
	Py_DECREF(pyFileName);

	if (pyModule == NULL) {
		LOG << "Failed to load Python module" << std::endl;
		Py_Finalize();
		return 0;
	}

	// Load the function from the module
	pyDbscan = PyObject_GetAttrString(pyModule, "run_dbscan");
	Py_DECREF(pyModule);

	if (pyDbscan == NULL || !PyCallable_Check(pyDbscan)) {
		if (PyErr_Occurred()) {
			PyErr_Print();
		}
		LOG << "Failed to load Python function" << std::endl;
		Py_XDECREF(pyDbscan);
		Py_Finalize();
		return 0;
	}

	return 1;
}

vector<int> CPFA_loop_functions::RunDBSCAN(std::vector<std::pair<double, double>> dataset){

	// LOG << "SearchRadius: " << SearchRadius << endl;
	PyObject* pyarg_Epsilon = PyFloat_FromDouble(SearchRadius); 
	PyObject* pyarg_MinSamples = PyLong_FromLong(2); 
	PyObject* pyarg_Dataset = PyList_New(0); // Assuming dataset is a std::vector<std::pair<double, double>>
	for (const auto& point : dataset) {
		PyObject* pytmp_Point = Py_BuildValue("(dd)", point.first, point.second);
		PyList_Append(pyarg_Dataset, pytmp_Point);
		Py_DECREF(pytmp_Point);
	}

	pyDbscanArgs = PyTuple_Pack(3, pyarg_Epsilon, pyarg_MinSamples, pyarg_Dataset);

	// Call the function with arguments
	pyCallDbscan = PyObject_CallObject(pyDbscan, pyDbscanArgs);
	// Py_DECREF(pyDbscan);
	Py_DECREF(pyDbscanArgs);
	Py_DECREF(pyarg_Epsilon);
	Py_DECREF(pyarg_MinSamples);
	Py_DECREF(pyarg_Dataset);

	if (pyCallDbscan == NULL) {
		PyErr_Print();
		throw std::runtime_error("Error calling Python function");
	}

	std::vector<int> labels;

    // Assuming pyCallDbscan is the PyObject* returned by calling the Python function
    if (PyList_Check(pyCallDbscan)) {
        Py_ssize_t listSize = PyList_Size(pyCallDbscan);

        for (Py_ssize_t i = 0; i < listSize; ++i) {
            PyObject* pLabel = PyList_GetItem(pyCallDbscan, i);
            int label = PyLong_AsLong(pLabel);
            labels.push_back(label);
        }
    }

    Py_DECREF(pyCallDbscan);

    return labels;
}

vector<pair<CVector2, int>>& CPFA_loop_functions::GetClusterList(){
	return clusterList;
}

REGISTER_LOOP_FUNCTIONS(CPFA_loop_functions, "CPFA_loop_functions")
