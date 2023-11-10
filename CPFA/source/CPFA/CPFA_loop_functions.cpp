#include "CPFA_loop_functions.h"
#include <Python.h>

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
	RateOfLayingPheromone(0.0),
	RateOfPheromoneDecay(0.0),
	FoodRadius(0.05),
	FoodRadiusSquared(0.0025),
	NestRadius(0.12),
	AtkNestRadius(NestRadius/2),
	NestRadiusSquared(0.0625),
	NestElevation(0.01),
	// We are looking at a 4 by 4 square (3 targets + 2*1/2 target gaps)
	SearchRadiusSquared((4.0 * FoodRadius) * (4.0 * FoodRadius)),
	SearchRadius(4.0*FoodRadius),
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
	numFalsePositives(0),
	numQZones(0),
	k(1)		// initially k = 1 (no effect on estimation)
{}

void CPFA_loop_functions::Init(argos::TConfigurationNode &node) {	
 
	argos::CDegrees USV_InDegrees;
	argos::TConfigurationNode CPFA_node = argos::GetNode(node, "CPFA");

	argos::GetNodeAttribute(CPFA_node, "ProbabilityOfSwitchingToSearching", ProbabilityOfSwitchingToSearching);
	argos::GetNodeAttribute(CPFA_node, "ProbabilityOfReturningToNest",      ProbabilityOfReturningToNest);
	argos::GetNodeAttribute(CPFA_node, "UninformedSearchVariation",         USV_InDegrees);
	argos::GetNodeAttribute(CPFA_node, "RateOfInformedSearchDecay",         RateOfInformedSearchDecay);
	argos::GetNodeAttribute(CPFA_node, "RateOfSiteFidelity",                RateOfSiteFidelity);
	argos::GetNodeAttribute(CPFA_node, "RateOfLayingPheromone",             RateOfLayingPheromone);
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
	// argos::GetNodeAttribute(settings_node, 'BotFwdSpeed',					BotFwdSpeed);
	argos::GetNodeAttribute(settings_node, "EstTravelTimeTolerance",		T_tolerance);
	FoodRadiusSquared = FoodRadius*FoodRadius;

	argos::TConfigurationNode atk_node = argos::GetNode(node, "detractor_settings");

	argos::GetNodeAttribute(atk_node, "NumAtkNests",					NumAtkNests);
	// argos::GetNodeAttribute(atk_node, "AtkNest1Position",				AtkNest1Position);
	// argos::GetNodeAttribute(atk_node, "AtkNest2Position",				AtkNest2Position);
	// argos::GetNodeAttribute(atk_node, "AtkNest3Position",				AtkNest3Position);
	// argos::GetNodeAttribute(atk_node, "AtkNest4Position",				AtkNest4Position);
	argos::GetNodeAttribute(atk_node, "AtkNestRadius",					AtkNestRadius);


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

	/**
	 * This is a test to see if I can execute python code in here.
	 */

	Py_Initialize();
	if(Py_IsInitialized()){
		// LOG << "Python version: " << Py_GetVersion() << endl;
	} else {
		LOGERR << "ERROR: Python failed to initialize." << endl;
		exit(1);
	}

	PyObject *pName, *pModule, *pFunc, *pCallFunc, *pArgs;
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
	pName = PyUnicode_FromString("cpfa_test");
	if (pName == NULL) {
		LOG << "Error converting module name to PyUnicode" << std::endl;
		Py_Finalize();
		return;
	}

	pModule = PyImport_Import(pName);
	Py_DECREF(pName);

	if (pModule == NULL) {
		LOG << "Failed to load Python module" << std::endl;
		Py_Finalize();
		return;
	}

	// Load the function from the module
	pFunc = PyObject_GetAttrString(pModule, "test_func");
	Py_DECREF(pModule);

	if (pFunc == NULL || !PyCallable_Check(pFunc)) {
		if (PyErr_Occurred()) {
			PyErr_Print();
		}
		LOG << "Failed to load Python function" << std::endl;
		Py_XDECREF(pFunc);
		Py_Finalize();
		return;
	}

	// Call the function
	pCallFunc = PyObject_CallObject(pFunc, NULL);
	Py_DECREF(pFunc);

	if (pCallFunc == NULL) {
		LOG << "Function call failed" << std::endl;
		Py_Finalize();
		return;
	}

	// Convert the result to C++ type and print
	Real func_out = PyFloat_AsDouble(pCallFunc);
	Py_DECREF(pCallFunc);

	LOG << "func_out: " << func_out << std::endl;

	Py_Finalize();

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
	// check pheromone list and certain frequency to see if robots are returning within time frame

	argos::CSpace::TMapPerType& footbots = GetSpace().GetEntitiesByType("foot-bot");

	// this is where we will check to see which trail a robot is following
	for (size_t i = 0; i < trailLog.size(); i++) {
		
		// here we do the math for travel time estimation
		CVector2 trailPos = get<1>(trailLog[i]).GetLocation();
		Real trailLength = sqrt( pow( abs(NestPosition.GetX()) - abs(trailPos.GetX()), 2) + pow( abs(NestPosition.GetY()) - abs(trailPos.GetY()), 2) );
		Real T_est = trailLength * 2 * k;	// multiply by 2 to get distance to and from the target location

		// get current travel time (current_time - start_time)
		Real cur_travel_time = getSimTimeInSeconds() - std::get<2>(trailLog[i]);

		if (cur_travel_time > (T_est * (1+T_tolerance))){
			// if the robot has taken too long to return, we will flag the bot as missing and form a vote against the creator of the trail

			// TODO: We will run the DBSCAN here, and start a vote against the creator of the trail and the creators of the neighboring trails (points) within its cluster.

			// TODO: We must keep in mind how to construct this code dynamically, so that we can create a graph of clusters whose edges represent common creator ids (e.g. atk_nests will likely have a lot of common creator ids between them).

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

		// Write to file ** Ryan Luna 11/17/22
		ofstream DataOut((FilenameHeader+"AttackData.txt").c_str(), ios::app);
		LOG << "Writing to file: " << FilenameHeader+"AttackData.txt" << endl;
		if (DataOut.tellp() == 0){

			DataOut 	<< "Simulation Time (seconds), Total Food Collected, Total Food Collection Rate (per second), " 
							<< "Total Robots Captured, Robots Captured (per second)" << endl;

							// << "Fake Food Collected, Fake Food Collection Rate (per second), " 
							// << "Real Food Trails Created, Fake Food Trails Created, False Positives, QZones" << endl;
		}

		TotalFoodCollected = RealFoodCollected + FakeFoodCollected;

		DataOut 	<< getSimTimeInSeconds() << ',' << TotalFoodCollected << ',' << TotalFoodCollected/getSimTimeInSeconds() << ','
						<< AttackerNest.GetNumCapturedRobots() << ',' << AttackerNest.GetNumCapturedRobots()/getSimTimeInSeconds() << endl;
						
						// << FakeFoodCollected << ',' << FakeFoodCollected/getSimTimeInSeconds() << ','
						// << numRealTrails << ',' << numFakeTrails << ',' << numFalsePositives << ',' << MainNest.GetZoneList().size() << endl;
      }

	ofstream TerminateCount ((FilenameHeader+"TerminatedCount.txt").c_str(), ios::app);
	if(terminate){
		TerminateCount	<< 0 << ", ";
	} else {
		TerminateCount	<< 1 << ", ";
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
		if(PheromoneList[i].IsActive()) {
			new_p_list.push_back(PheromoneList[i]);
		} else {
			inactivePheromoneList.push_back(PheromoneList[i]);
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
	return RateOfLayingPheromone;
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
	RateOfLayingPheromone             = g[5];
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

						CVector3 newPosition = GenEntityPosition();
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

							newPosition = GenEntityPosition();

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

					LOG << footBot.GetId() << ": Captured and moved." << endl;

				} else {
					LOG << "CPFA_controller cast failed." << endl;
				}
			} else {
				LOG << "BaseController cast failed." << endl;
			}
		}
	}

}

CVector3 CPFA_loop_functions::GenEntityPosition(){
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
			LOG << "Too close to robot " << footBot.GetId() << endl;
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
		}
	}
}

vector<CVector3> CPFA_loop_functions::GetAtkNestList(){
	vector<CVector3> AtkNestList3d;
	for (CVector2 atkNestPos : AtkNestPositions){
		AtkNestList3d.push_back(CVector3(atkNestPos.GetX(), atkNestPos.GetY(), 0.0));
	}
	return AtkNestList3d;
}

REGISTER_LOOP_FUNCTIONS(CPFA_loop_functions, "CPFA_loop_functions")
