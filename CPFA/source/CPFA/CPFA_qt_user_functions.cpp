#include "CPFA_qt_user_functions.h"

/*****
 * Constructor: In order for drawing functions in this class to be used by
 * ARGoS it must be registered using the RegisterUserFunction function.
 *****/
CPFA_qt_user_functions::CPFA_qt_user_functions() :
	loopFunctions(dynamic_cast<CPFA_loop_functions&>(CSimulator::GetInstance().GetLoopFunctions()))
{
	RegisterUserFunction<CPFA_qt_user_functions, CFootBotEntity>(&CPFA_qt_user_functions::DrawOnRobot);
	RegisterUserFunction<CPFA_qt_user_functions, CFloorEntity>(&CPFA_qt_user_functions::DrawOnArena);
}

void CPFA_qt_user_functions::DrawOnRobot(CFootBotEntity& entity) {
	CPFA_controller& c = dynamic_cast<CPFA_controller&>(entity.GetControllableEntity().GetController());

	// modified to draw fake food	** Ryan Luna 11/12/22
	if(c.IsHoldingFood()) {
		if(c.IsHoldingFakeFood()){
			DrawCylinder(CVector3(0.0, 0.0, 0.3), CQuaternion(), loopFunctions.FoodRadius, 0.025, CColor::PURPLE);	
		} else {
			DrawCylinder(CVector3(0.0, 0.0, 0.3), CQuaternion(), loopFunctions.FoodRadius, 0.025, CColor::BLACK);
		}
		
	}

	if(loopFunctions.DrawIDs == 1) {
		/* Disable lighting, so it does not interfere with the chosen text color */
		glDisable(GL_LIGHTING);
		/* Disable face culling to be sure the text is visible from anywhere */
		glDisable(GL_CULL_FACE);
		/* Set the text color */
		CColor cColor(CColor::BLACK);
		glColor3ub(cColor.GetRed(), cColor.GetGreen(), cColor.GetBlue());

		/* The position of the text is expressed wrt the reference point of the footbot
		 * For a foot-bot, the reference point is the center of its base.
		 * See also the description in
		 * $ argos3 -q foot-bot
		 */
		
		// Disable for now
		//GetOpenGLWidget().renderText(0.0, 0.0, 0.5,             // position
		//			     entity.GetId().c_str()); // text
		
			DrawText(CVector3(0.0, 0.0, 0.3),   // position
            entity.GetId().c_str()); // text
		/* Restore face culling */
		glEnable(GL_CULL_FACE);
		/* Restore lighting */
		glEnable(GL_LIGHTING);
	}
}
 
void CPFA_qt_user_functions::DrawOnArena(CFloorEntity& entity) {
	DrawFood();
	DrawFidelity();
	DrawPheromones();
	DrawNest();
	DrawQuarantineZone();

	if(loopFunctions.DrawTargetRays == 1) DrawTargetRays();
}

/*****
 * This function is called by the DrawOnArena(...) function. If the iAnt_data
 * object is not initialized this function should not be called.
 *****/
void CPFA_qt_user_functions::DrawNest() {
	/* 2d cartesian coordinates of the nest */
	Real x_coordinate = loopFunctions.NestPosition.GetX();
	Real y_coordinate = loopFunctions.NestPosition.GetY();

	/* required: leaving this 0.0 will draw the nest inside of the floor */
	Real elevation = loopFunctions.NestElevation;

	/* 3d cartesian coordinates of the nest */
	CVector3 nest_3d(x_coordinate, y_coordinate, elevation);

	/* Draw the nest on the arena. */
	//DrawCircle(nest_3d, CQuaternion(), loopFunctions.NestRadius, CColor::RED);
    DrawCylinder(nest_3d, CQuaternion(), loopFunctions.NestRadius, 0.008, CColor::GREEN);
}

void CPFA_qt_user_functions::DrawQuarantineZone() {			// Ryan Luna 1/24/23

	vector<QZone> zonelist = loopFunctions.MainNest.GetZoneList();

	for(int i=0;i<zonelist.size();i++){
		/* 2d cartesian coordinates of the zone */
		Real x_coordinate = zonelist[i].GetLocation().GetX();
		Real y_coordinate = zonelist[i].GetLocation().GetY();

		/* required: leaving this 0.0 will draw the zone inside of the floor */
		Real elevation = 0.0;

		/* 3d cartesian coordinates of the zone */
		CVector3 nest_3d(x_coordinate, y_coordinate, elevation);

		/* Draw the zone on the arena. */
		DrawCylinder(nest_3d, CQuaternion(), zonelist[i].GetRadius(), 0.008, zonelist[i].GetColor());
	}
	zonelist.clear();
}

void CPFA_qt_user_functions::DrawFood() {

	Real x, y;

	// modified ** Ryan Luna 11/11/22
	for(size_t i = 0; i < loopFunctions.FoodList.size(); i++) {
		x = loopFunctions.FoodList[i].GetLocation().GetX();
		y = loopFunctions.FoodList[i].GetLocation().GetY();
		DrawCylinder(CVector3(x, y, 0.002), CQuaternion(), loopFunctions.FoodRadius, 0.025, loopFunctions.FoodList[i].GetColor());
	}

	// shouldn't need the following loop as CollectedFoodList is not maintained anyway ** Ryan Luna 11/11/22
 
	//draw food in nests
	// for (size_t i=0; i< loopFunctions.CollectedFoodList.size(); i++)
	// { 
	//         x = loopFunctions.CollectedFoodList[i].GetX();
	//         y = loopFunctions.CollectedFoodList[i].GetY();
	//         DrawCylinder(CVector3(x, y, 0.002), CQuaternion(), loopFunctions.FoodRadius, 0.025, CColor::BLACK);
	// }
}

void CPFA_qt_user_functions::DrawFidelity() {

	   Real x, y;
        for(map<string, CVector2>::iterator it= loopFunctions.FidelityList.begin(); it!=loopFunctions.FidelityList.end(); ++it) {
            x = it->second.GetX();
            y = it->second.GetY();
            DrawCylinder(CVector3(x, y, 0.0), CQuaternion(), loopFunctions.FoodRadius, 0.025, CColor::YELLOW);
        }
}

void CPFA_qt_user_functions::DrawPheromones() {

	Real x, y, weight;
	vector<CVector2> trail;
	CColor trailColor = CColor::GREEN, pColor = CColor::GREEN;

	    for(size_t i = 0; i < loopFunctions.PheromoneList.size(); i++) {
		       x = loopFunctions.PheromoneList[i].GetLocation().GetX();
		       y = loopFunctions.PheromoneList[i].GetLocation().GetY();

		       if(loopFunctions.DrawTrails == 1) {
			          trail  = loopFunctions.PheromoneList[i].GetTrail();
			          weight = loopFunctions.PheromoneList[i].GetWeight();
                

             if(weight > 0.25 && weight <= 1.0)        // [ 100.0% , 25.0% )
                 pColor = trailColor = CColor::GREEN;
             else if(weight > 0.05 && weight <= 0.25)  // [  25.0% ,  5.0% )
                 pColor = trailColor = CColor::YELLOW;
             else                                      // [   5.0% ,  0.0% ]
                 pColor = trailColor = CColor::RED;
      
             CRay3 ray;
             size_t j = 0;
      
             for(j = 1; j < trail.size(); j++) {
                 ray = CRay3(CVector3(trail[j - 1].GetX(), trail[j - 1].GetY(), 0.01),
		CVector3(trail[j].GetX(), trail[j].GetY(), 0.01));
                 
                 DrawRay(ray, trailColor, 1.0);
             }

	 DrawCylinder(CVector3(x, y, 0.0), CQuaternion(), loopFunctions.FoodRadius, 0.025, pColor);
		       } 
         else {
			          weight = loopFunctions.PheromoneList[i].GetWeight();

             if(weight > 0.25 && weight <= 1.0)        // [ 100.0% , 25.0% )
                 pColor = CColor::GREEN;
             else if(weight > 0.05 && weight <= 0.25)  // [  25.0% ,  5.0% )
                 pColor = CColor::YELLOW;
             else                                      // [   5.0% ,  0.0% ]
                 pColor = CColor::RED;
      
             DrawCylinder(CVector3(x, y, 0.0), CQuaternion(), loopFunctions.FoodRadius, 0.025, pColor);
         }
 }
}

void CPFA_qt_user_functions::DrawTargetRays() {
	//size_t tick = loopFunctions.GetSpace().GetSimulationClock();
	//size_t tock = loopFunctions.GetSimulator().GetPhysicsEngine("default").GetInverseSimulationClockTick() / 8;

	//if(tock == 0) tock = 1;

	//if(tick % tock == 0) {
		for(size_t j = 0; j < loopFunctions.TargetRayList.size(); j++) {
			DrawRay(loopFunctions.TargetRayList[j], loopFunctions.TargetRayColorList[j]);
		}
	//}
}

/*
void CPFA_qt_user_functions::DrawTargetRays() {

	CColor c = CColor::BLUE;

	for(size_t j = 0; j < loopFunctions.TargetRayList.size(); j++) {
			DrawRay(loopFunctions.TargetRayList[j],c);
	}

	//if(loopFunctions.SimTime % (loopFunctions.TicksPerSecond * 10) == 0) {
		// comment out for DSA, uncomment for CPFA
		loopFunctions.TargetRayList.clear();
	//}
}
*/

REGISTER_QTOPENGL_USER_FUNCTIONS(CPFA_qt_user_functions, "CPFA_qt_user_functions")
