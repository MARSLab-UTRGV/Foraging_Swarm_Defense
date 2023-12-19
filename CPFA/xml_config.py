from xml.dom import minidom
import math

####### GLOBAL CONSTANTS (DON'T MODIFY) #######

H_C = 0.288699733

###############################################

class C_XML_CONFIG:
    
    def __init__ (self, iterations):

        self.PFS = "1"                           # Print Final Score

        self.XML_FNAME = "./experiments/Misleading_Trail_1.xml"



        # Default distribution parameters are for Random Distribution
        # Use setDistribution() to use the correct parameters for the
        # desirred distribution mode.

        self.PRN    = "0.0147598869881"             # Probability Of Returning To Nest
        self.PSS    = "0.723128706375"              # Probability Of Switching To Searching
        self.RISD   = "0.205799848158"              # Rate Of Informed Search Decay
        self.RLP    = "14.7027566005"               # Rate of Laying Pheromone
        self.RPD    = "0.0245057227138"             # Rate Of Pheromone Decay
        self.RSF    = "14.1514206414"               # Rate Of Site Fidelity
        self.USV    = "2.81939731297"               # Uninformed Search Variation


        ####### CONFIGURATION #######

        self.BOT_DEFAULT_DIST =  True                    # Use default distribution found in original CPFA tests
                                                         # If this method is used, self.BOT_COUNT is ignored and 24 bots
                                                         # will be used instead in grid distribution mode
        self.USE_MISLEADING_TRAIL_ATTACK = False         # Use misleading trail attack

        self.T_BOT_COUNT =       32                      # total bot count
        self.D_BOT_COUNT =       0                       # detractor bot count
        self.BOT_COUNT =         self.T_BOT_COUNT        # normal bot count (not detractors)
        self.BOTS_PER_GROUP =    self.BOT_COUNT/4        # number of bots per group * DEFAULT DISTRIBUTION ONLY*
        self.BOT_DIST_RAD =      1.5                     # Bot distribution radius (uniform distribution in central area)
        self.BOT_LAYOUT =        (2,4)                   # Bot layout (x,y) * DEFAULT DISTRIBUTION ONLY*
        self.D_BOT_LAYOUT =      (0,0)                   # Detractor bot layout (x,y) * DEFAULT DISTRIBUTION ONLY*

        self.ARENA_SIZE =        (10,10,1)               # (x,y,z) foraging area size
        self.TOTAL_SIZE =        (12,10,1)               # to allow space for holding area for capture bots

        # Visualization Settings
        self.CAM_HEIGHT =        35                      # simulation camera height
        self.VISUAL =            True                    # turn on/off visual simulator

        # General Config
        self.THREAD_COUNT =      0
        self.SIM_LENGTH =        6000                    # length of experiment in seconds
        self.RANDOM_SEED =       0
        self.TPS =               16                      # ticks/steps per second

        # Controller Sensor Settings
        self.SHOW_PROX_RAYS =    "true"                  # turn on/off footbot proximity sensor rays

        # Contoller Parameter Settings 
        self.DN_SD =             0.00                    # Destination Noise Standard Deviation
        self.FDT =               0.13                    # Food Distance Tolerance
        self.NAT =               0.10                    # Nest Angle Tolerance
        self.NDT =               0.05                    # Nest Distance Tolerance
        self.PN_SD =             0.00                    # Position Noise Standard Deviation
        self.RD_PATH =           "results/"              # results directory path
        self.BOT_FW_SPD =        16.00                   # robot forward speed
        self.BOT_ROT_SPD =       8.00                    # robot rotation speed
        self.SSS =               0.08                    # Search Step Size
        self.TAT =               0.10                    # Target Angle Tolerance
        self.TDT =               0.05                    # Target Distance Tolerance
        self.UQZ =               'false'                 # Turn ON/OFF QZone usage
        self.MM =                1                       # Merge Mode (0->No Merging, 1->Distance-Based)
        self.FF_ACC=             1.00                    # Food Food Accuracy (0.0-1.0)
        self.RF_ACC=             1.00                    # Real Food Food Accuracy (0.0-1.0)

        # Fake Food Loop Function Settings **
        self.USE_FF_DOS =        "false"                 # Turn on/off fake_food DoS
        self.FFD =               0                       # Fake Food Distribution Mode (0=Random, 1=Cluster, 2=PowerLaw) (default = Random)
        self.NUM_FF =            64                      # Number of fake food to distribute for random distribution
        self.NUM_FCL =           1                       # Number of fake food clusters for cluster distribution
        self.FCL_X =             8                       # Fake cluster width X for cluster distribution
        self.FCL_Y =             8                       # Fake cluster width Y for cluster distribution
        self.NUM_PLAW_FF =       64                      # Number of fake food to distribute for power law distribution
        self.USE_ALT_DIST =      "false"                 # Use alternate fake food distribution (4 3x12 clusters on each wall)
        self.ALT_FCL_W =         36                      # Alternate fake food cluster width (using alt dist only)
        self.ALT_FCL_L =         4                       # Alternate fake food cluster length (using alt dist only)
        self.USE_FF_ONLY =       'false'                 # Turn on/off fake food only mode (0=No, 1=Yes) (default = No)

        # Real Food Loop Function Settings
        self.RFD =               0                       # Real Food Distribution Mode (0=Random, 1=Cluster, 2=PowerLaw) (default = Random)
        self.NUM_RF =            192                      # Number of real food to distribute for random distribution
        self.NUM_RCL =           2                       # Number of real food clusters for cluster distribution
        self.RCL_X =             8                       # Real cluster width X for cluster distribution
        self.RCL_Y =             8                       # Real cluster width Y for cluster distribution
        self.NUM_PLAW_RF =       192                     # Number of real food to distribute for power law distribution

        # Other Loop Function Settings
        self.DRAW_ID =           1                       # Draw bot IDs
        self.DRAW_TARGET_RAYS =  0                       # Draw directional rays to target (for each bot)
        self.DRAW_TRAILS =       0                       # Draw pheromone trails
        self.DRAW_DENSITY_RATE = 4                       # Draw density rate of resources
        self.MAX_SIM_COUNT =     1                       # Max simulation counter
        self.MAX_SIM_TIME =      1800                    # Max simulation time in seconds
        self.OUTPUT_DATA =       0                       # turn output data on/off
        self.NEST_ELV =          0.001                   # Nest elevation
        self.NEST_POS =          (0,0)                   # Nest location

        atkNest_x = self.ARENA_SIZE[0]/2-1
        atkNest_y = self.ARENA_SIZE[1]/2-1
        self.ATK_NEST1_POS =      (atkNest_x,atkNest_y)         # Attacker nest_1 location
        self.ATK_NEST2_POS =      (-atkNest_x,atkNest_y)        # Attacker nest_2 location
        self.ATK_NEST3_POS =      (-atkNest_x,-atkNest_y)       # Attacker nest_3 location
        self.ATK_NEST4_POS =      (atkNest_x,-atkNest_y)        # Attacker nest_4 location
        self.NUM_DETRACTORS_NEST1 =   0                         # Number of detractor robots in nest_1
        self.NUM_DETRACTORS_NEST2 =   0                         # Number of detractor robots in nest_2
        self.NUM_DETRACTORS_NEST3 =   0                         # Number of detractor robots in nest_3
        self.NUM_DETRACTORS_NEST4 =   0                         # Number of detractor robots in nest_4
        self.USE_MTATK =            "false"                     # Turn on/off misleading trail attack
        self.NUM_ATK_NESTS =    1                               # Number of attacker nests (MAX = 4)
        self.RAND_ATK_NEST =    "true"                         # Randomize attacker nest location
        
        self.NEST_RAD =          0.25                    # Nest radius
        self.ATK_NEST_RAD =      self.NEST_RAD/2         # Attacker nest radius

        self.VFP =               0                       # Variable food placement
        self.FOOD_RAD =          0.05                    # Food radius
        self.DENSIFY =           "false"                 # Turn ON/OFF dense clusters

        self.fname_header = "\0"                         # Filename Header
        self.num_iterations = iterations                 # Number of Experiment Iterations

        self.LET_DET_USE_MLT =  "true"                 # Let detractors use misleading trails

        ########### Defense Parameters ###########
        self.USE_DEF =           "false"                 # Turn on/off defense
        self.USE_DEF_RB =        "false"                 # Turn on/off return boolean for defense
        self.USE_DEF_CL =        "false"                 # Turn on/off trail clustering for defense
        self.USE_DEF_CG =        "false"                 # Turn on/off cluster graph for defense
        self.FLW =               0.0                     # Feedback Loop Weight (0-1)
        self.STRIKE_LIMIT =      3                       # Strike limit (number of strikes before a bot gets isolated)
        self.TTT =               0.15                    # Travel Time Tolerance
        self.USFB =              "false"                 # Use feedback equation (if false, use unified velocity)

        ########### Attack Analysis Experiments ###########
        self.USE_RATIO_CHECK =   "false"                 # Turn on/off ratio check experiment
        self.RATIO_CHECK_FREQ =  10                      # Ratio check frequency (seconds)

    def UseDefenseMethod(self, useDef):
        if (useDef):
            self.USE_DEF = 'true'
        else:
            self.USE_DEF = 'false'
    
    def UseDefenseReturnBoolean(self, useDefRB):
        if (useDefRB):
            self.USE_DEF_RB = 'true'
        else:
            self.USE_DEF_RB = 'false'

    def UseDefenseClustering(self, useDefCL):
        if (useDefCL):
            self.USE_DEF_CL = 'true'
        else:
            self.USE_DEF_CL = 'false'
    
    def UseDefenseClusterGraph(self, useDefCG):
        if (useDefCG):
            self.USE_DEF_CG = 'true'
        else:
            self.USE_DEF_CG = 'false'

    def setDetractorPercentage(self, percent, static_foragers=False):
        if percent > 100 or percent < 0:
            raise Exception("ERROR: Invalid detractor percentage given...")

        if not static_foragers:
            # Detractors are a percentage of the total bots (self.T_BOT_COUNT)
            # Total bots remain constant
            self.D_BOT_COUNT = math.floor(self.T_BOT_COUNT * (percent / 100))
            self.BOT_COUNT = self.T_BOT_COUNT - self.D_BOT_COUNT
        else:
            # Detractors are a percentage of the base number of foragers (self.BOT_COUNT)
            # Total bots (foragers + detractors) increase as detractors increase
            self.D_BOT_COUNT = math.floor(self.BOT_COUNT * (percent / 100))
            # Calculate the total bot count by adding the number of detractors
            self.TOTAL_BOT_COUNT = self.BOT_COUNT + self.D_BOT_COUNT

        self.BOTS_PER_GROUP = self.BOT_COUNT / 4

    def genBotLayouts(self, groups=4):
        # Calculate the number of bots for each group
        bots_per_group = [self.BOT_COUNT // groups + (1 if x < self.BOT_COUNT % groups else 0) for x in range(groups)]
        
        # Initialize an empty list to hold tuples of layout strings and bot counts
        layout_info = []
        
        # Define a function to calculate the layout for a given count
        def calculate_layout(count):
            if count < 4:
                # If we have less than 4 bots, we just place them in a single row.
                return 1, count
            # We start looking for factors from the square root downward
            for i in range(int(count**0.5), 1, -1):
                if count % i == 0:
                    return i, count // i
            # If no factor pair was found and the number is prime or nearly prime,
            # we force a 2-row layout for numbers greater than 3.
            return 2, (count + 1) // 2

        # Calculate the layout for each group of normal bots
        for count in bots_per_group:
            x, y = calculate_layout(count)
            layout_string = f"{x},{y},1"
            layout_info.append((layout_string, count))

        # Calculate the layout for the detractor group (assuming it's a single group)
        x, y = calculate_layout(self.D_BOT_COUNT)
        detractor_layout_string = f"{x},{y},1"
        layout_info.append((detractor_layout_string, self.D_BOT_COUNT))

        # Return the list of tuples
        return layout_info

    def setDistribution(self, distribution):
        if distribution == 0:   # random
            self.PRN    = "0.0147598869881"             # Probability Of Returning To Nest
            self.PSS    = "0.723128706375"              # Probability Of Switching To Searching
            self.RISD   = "0.205799848158"              # Rate Of Informed Search Decay
            self.RLP    = "14.7027566005"               # Rate of Laying Pheromone
            self.RPD    = "0.0245057227138"             # Rate Of Pheromone Decay
            self.RSF    = "14.1514206414"               # Rate Of Site Fidelity
            self.USV    = "2.81939731297"               # Uninformed Search Variation

            self.RFD    = 0                             # Real Food Distribution Mode
            self.FFD    = 0                             # Fake Food Distribution Mode

        elif distribution == 1:  # cluster
            self.PSS     = "0.3637176255"
            self.PRN     = "0.00297618325581"
            self.USV     = "2.67338576954"
            self.RISD    = "0.253110502082"
            self.RSF     = "1.42036207003"
            # self.RLP     = "8.98846470854"
            self.RLP     = "1.0"                    # For increased pheromone laying rate (Nov 10, 2023)
            self.RPD     = "0.063119269938"

            self.RFD    = 1
            self.FFD    = 1

        elif distribution == 2:  # powerlaw
            self.PSS     = "0.3637176255"
            self.PRN     = "0.00297618325581"
            self.USV     = "2.67338576954"
            self.RISD    = "0.253110502082"
            self.RSF     = "1.42036207003"
            self.RLP     = "15.976929417"
            self.RPD     = "0.063119269938"

            self.RFD     = 2
            self.FFD     = 2
        else:
            raise Exception("ERROR: A valid distribution mode was not given...")

    def UseFFDoS(self, useFF):
        if (useFF):
            if(self.USE_FF_ONLY == "true"):
                print("ERROR: Cannot use FF Only and FF DoS at the same time...")
                exit(1)
            self.USE_FF_DOS = 'true'
        else:
            self.USE_FF_DOS = 'false'
        
    def UseQZone(self, useQZ):
        if (useQZ):
            self.UQZ = "true"
        else:
            self.UQZ = "false"

    def UseMisleadingTrailAttack(self, useMTA):
        if (useMTA):
            self.USE_MTATK = "true"
            self.USE_MISLEADING_TRAIL_ATTACK = True
        else:
            self.USE_MTATK = "false"
            self.USE_MISLEADING_TRAIL_ATTACK = False
    
    def Densify(self, dense):
        if dense:
            self.DENSIFY = "true"
        else:
            self.DENSIFY = "false"

    def UseAltDistribution(self, useAlt):
        if (useAlt):
            self.USE_ALT_DIST = 'true'
        else:
            self.USE_ALT_DIST = 'false'
    
    def UseFFOnly(self, useFFOnly):
        if (useFFOnly):
            if (self.USE_FF_DOS == 'true'):
                print("ERROR: Cannot use FF Only and use FF DoS at the same time...")
                exit(1)
            self.USE_FF_ONLY = 'true'
        else:
            self.USE_FF_ONLY = 'false'

    # generates arena size string for xml based on self.ARENA_SIZE
    def arenaSize(self):
        return str(self.TOTAL_SIZE[0])+','+str(self.TOTAL_SIZE[1])+','+str(self.TOTAL_SIZE[2])
    
    def foragingAreaSize(self):
        return str(self.ARENA_SIZE[0])+','+str(self.ARENA_SIZE[1])+','+str(self.ARENA_SIZE[2])

    # generates wall size string for each wall face based on self.ARENA_SIZE
    def wallSize(self, face):
        if (face.lower() == 'north' or face.lower() == 'south'):
            return str(self.ARENA_SIZE[0])+',0.1,0.5'
        elif (face.lower() == 'east' or face.lower() == 'west'):
            return '0.1,'+str(self.ARENA_SIZE[1])+',0.5'
        else:
            raise Exception("ERROR: A valid wall name was not given...")

    # generates wall position string for each wall face based on self.ARENA_SIZE
    def wallPosition(self, face):
        if face.lower() == 'north':
            return '0,'+str(self.ARENA_SIZE[0]/2)+',0'
        elif face.lower() == 'south':
            return '0,-'+str(self.ARENA_SIZE[0]/2)+',0'
        elif face.lower() == 'east':
            return str(self.ARENA_SIZE[1]/2)+',0,0'
        elif face.lower() == 'west':
            return '-'+str(self.ARENA_SIZE[1]/2)+',0,0'
        else:
            raise Exception("ERROR: A valid wall name was not given...")

    # for uniform distribution method based on self.ARENA_SIZE
    def botUPosition(self, limit):
        if limit.lower() == 'min':
            return str(-self.ARENA_SIZE[0]/2)+','+str(-self.ARENA_SIZE[1]/2)+',0'
        elif limit.lower() == 'max':
            return str(self.ARENA_SIZE[0]/2)+','+str(self.ARENA_SIZE[1]/2)+',0'
        else:
            raise Exception("ERROR: limit name unidentified for botUPosition()\n")
        
    def getNumDetractors(self):
        return self.NUM_DETRACTORS_NEST1+self.NUM_DETRACTORS_NEST2+self.NUM_DETRACTORS_NEST3+self.NUM_DETRACTORS_NEST4

    def setFname(self):

        dist = ''
        num_real_food = 0
        dense = ''
        
        if self.RFD == 0:
            dist = 'R-rand'
            num_real_food = self.NUM_RF
        
        elif self.RFD == 1:
            dist = 'R-cl'
            num_real_food = self.RCL_X * self.RCL_Y * self.NUM_RCL
       
        elif self.RFD == 2:
            dist = 'R-pl'
            num_real_food = self.NUM_PLAW_RF

        else:
            raise Exception("ERROR: Invalid distribution method used.\n")

        if self.DENSIFY == "true":
            dense = 'density-high'
        else:
            dense = 'density-std'

        path = self.RD_PATH
        alg = f'CPFA'
        bot_count = f'r{self.T_BOT_COUNT}'
        detractor_count = f'd{self.D_BOT_COUNT}'
        atk_nest_count = f'atk{self.NUM_ATK_NESTS}'
        rlp = f'rlp{self.RLP}'
        rfc = f'rfc{num_real_food}'
        arena = f'{self.ARENA_SIZE[0]}by{self.ARENA_SIZE[1]}'
        time = f'time{self.MAX_SIM_TIME}'
        iter = f'iter{self.num_iterations}'
        ttt = f'ttt{self.TTT}'

        self.fname_header = f'{path}{alg}_{dense}_{dist}_{bot_count}_{detractor_count}_{ttt}_{rlp}_{rfc}_{arena}_{time}_{iter}_'

        return self.fname_header

    def setBotCount(self,botCount):
        if not botCount % 4 == 0:
            print ("Warning: Number of bots not divisible by 4. Default bot distribution not supported...\n\n")
        self.T_BOT_COUNT = botCount
        self.BOTS_PER_GROUP = botCount/4

    def createXML(self):

        if (self.FLW < 0 or self.FLW > 1):
            raise Exception("ERROR: Feedback Loop Weight must be between 0 and 1...\n")

        self.setFname()

        xml = minidom.Document()

        # <argos-configuration>
        argos_config = xml.createElement('argos-configuration')
        xml.appendChild(argos_config)

        #   <framework>
        framework = xml.createElement('framework')
        argos_config.appendChild(framework)

        #       <system>
        system = xml.createElement('system')
        system.setAttribute('threads', str(self.THREAD_COUNT))
        framework.appendChild(system)
        #       <experiment>
        experiment = xml.createElement('experiment')
        experiment.setAttribute('length', str(self.SIM_LENGTH))
        experiment.setAttribute('ticks_per_second',str(self.TPS))
        experiment.setAttribute('random_seed', str(self.RANDOM_SEED))
        framework.appendChild(experiment)
        #   </framework>

        #   <controllers>
        controllers = xml.createElement('controllers')
        argos_config.appendChild(controllers)

        #       <CPFA_controller>
        cpfa_controller = xml.createElement('CPFA_controller')
        cpfa_controller.setAttribute('id','CPFA')
        cpfa_controller.setAttribute('library','build/source/CPFA/libCPFA_controller')
        controllers.appendChild(cpfa_controller)

        #           <actuators>
        actuators = xml.createElement('actuators')
        cpfa_controller.appendChild(actuators)

        #               <differential_steering>
        dif_steering = xml.createElement('differential_steering')
        dif_steering.setAttribute('implementation','default')
        actuators.appendChild(dif_steering)

        #               <leds>
        leds = xml.createElement('leds')
        leds.setAttribute('implementation','default')
        leds.setAttribute('medium','leds')
        actuators.appendChild(leds)
        #           </actuators

        #           <sensors>
        sensors = xml.createElement('sensors')
        cpfa_controller.appendChild(sensors)

        #               <footbot_proximity>
        fb_prox = xml.createElement('footbot_proximity')
        fb_prox.setAttribute('implementation','default')
        fb_prox.setAttribute('show_rays',str(self.SHOW_PROX_RAYS))
        sensors.appendChild(fb_prox)

        #               <positioning>
        fb_positioning = xml.createElement('positioning')
        fb_positioning.setAttribute('implementation','default')
        sensors.appendChild(fb_positioning)

        #               <footbot_motor_ground>
        fb_mg = xml.createElement('footbot_motor_ground')
        fb_mg.setAttribute('implementation','rot_z_only')
        sensors.appendChild(fb_mg)
        #           </sensors

        #           <params>
        params = xml.createElement('params')
        cpfa_controller.appendChild(params)

        #               <settings>
        params_settings = xml.createElement('settings')
        params_settings.setAttribute('DestinationNoiseStdev', str(self.DN_SD))
        params_settings.setAttribute('FoodDistanceTolerance', str(self.FDT))
        params_settings.setAttribute('NestAngleTolerance', str(self.NAT))
        params_settings.setAttribute('NestDistanceTolerance', str(self.NDT))
        params_settings.setAttribute('PositionNoiseStdev', str(self.PN_SD))
        params_settings.setAttribute('ResultsDirectoryPath', self.RD_PATH)
        params_settings.setAttribute('RobotForwardSpeed', str(self.BOT_FW_SPD))
        params_settings.setAttribute('RobotRotationSpeed', str(self.BOT_ROT_SPD))
        params_settings.setAttribute('SearchStepSize', str(self.SSS))
        params_settings.setAttribute('TargetAngleTolerance', str(self.TAT))
        params_settings.setAttribute('TargetDistanceTolerance', str(self.TDT))
        params_settings.setAttribute('UseQZones', str(self.UQZ))
        params_settings.setAttribute('MergeMode', str(self.MM))
        params_settings.setAttribute('FFdetectionAcc', str(self.FF_ACC))
        params_settings.setAttribute('RFdetectionAcc', str(self.RF_ACC))
        params_settings.setAttribute('UseMisleadingTrailAttack', str(self.USE_MTATK))
        params_settings.setAttribute('RandomizeAtkNest', str(self.RAND_ATK_NEST))
        params_settings.setAttribute('LetDetractorUseMLTrail', str(self.LET_DET_USE_MLT))
        params_settings.setAttribute('AtkNest1Position', f'{self.ATK_NEST1_POS[0]:.1f},{self.ATK_NEST1_POS[1]:.1f}')
        params_settings.setAttribute('AtkNest2Position', f'{self.ATK_NEST2_POS[0]:.1f},{self.ATK_NEST2_POS[1]:.1f}')
        params_settings.setAttribute('AtkNest3Position', f'{self.ATK_NEST3_POS[0]:.1f},{self.ATK_NEST3_POS[1]:.1f}')
        params_settings.setAttribute('AtkNest4Position', f'{self.ATK_NEST4_POS[0]:.1f},{self.ATK_NEST4_POS[1]:.1f}')
        params.appendChild(params_settings)
        #           </params>
        #       </CPFA_controller>
        #   </controllers>

        #   <loop_functions>
        loops = xml.createElement('loop_functions')
        loops.setAttribute('label','CPFA_loop_functions')
        loops.setAttribute('library','build/source/CPFA/libCPFA_loop_functions')
        argos_config.appendChild(loops)

        #       <CPFA>
        lf_cpfa = xml.createElement('CPFA')
        lf_cpfa.setAttribute('PrintFinalScore', str(self.PFS))
        lf_cpfa.setAttribute('ProbabilityOfReturningToNest', str(self.PRN))
        lf_cpfa.setAttribute('ProbabilityOfSwitchingToSearching', str(self.PSS))
        lf_cpfa.setAttribute('RateOfInformedSearchDecay', str(self.RISD))
        lf_cpfa.setAttribute('RateOfLayingPheromone', str(self.RLP))
        lf_cpfa.setAttribute('RateOfPheromoneDecay', str(self.RPD))
        lf_cpfa.setAttribute('RateOfSiteFidelity', str(self.RSF))
        lf_cpfa.setAttribute('UninformedSearchVariation', str(self.USV))
        loops.appendChild(lf_cpfa)
        #       </CPFA>

        #       <settings>
        lf_settings = xml.createElement('settings')
        lf_settings.setAttribute('DrawIDs', str(self.DRAW_ID))
        lf_settings.setAttribute('DrawTargetRays', str(self.DRAW_TARGET_RAYS))
        lf_settings.setAttribute('DrawTrails', str(self.DRAW_TRAILS))
        lf_settings.setAttribute('DrawDensityRate', str(self.DRAW_DENSITY_RATE))
        lf_settings.setAttribute('MaxSimCounter', str(self.MAX_SIM_COUNT))
        lf_settings.setAttribute('MaxSimTimeInSeconds', str(self.MAX_SIM_TIME))
        lf_settings.setAttribute('OutputData', str(self.OUTPUT_DATA))
        lf_settings.setAttribute('NestElevation', str(self.NEST_ELV))
        lf_settings.setAttribute('NestPosition', str(self.NEST_POS))
        lf_settings.setAttribute('NestRadius', str(self.NEST_RAD))
        lf_settings.setAttribute('VariableFoodPlacement', str(self.VFP))
        lf_settings.setAttribute('FoodRadius', str(self.FOOD_RAD))
        lf_settings.setAttribute('UseFakeFoodOnly', str(self.USE_FF_ONLY))
        lf_settings.setAttribute('FoodDistribution', str(self.RFD))
        lf_settings.setAttribute('UseAltDistribution', str(self.USE_ALT_DIST))
        lf_settings.setAttribute('AltClusterWidth', str(self.ALT_FCL_W))
        lf_settings.setAttribute('AltClusterLength', str(self.ALT_FCL_L))
        lf_settings.setAttribute('NumRealFood', str(self.NUM_RF))
        lf_settings.setAttribute('PowerlawFoodUnitCount', str(self.NUM_PLAW_RF))
        lf_settings.setAttribute('NumberOfClusters', str(self.NUM_RCL))
        lf_settings.setAttribute('ClusterWidthX', str(self.RCL_X))
        lf_settings.setAttribute('ClusterWidthY', str(self.RCL_Y))
        lf_settings.setAttribute('UseFakeFoodDoS', str(self.USE_FF_DOS))
        lf_settings.setAttribute('FakeFoodDistribution', str(self.FFD))
        lf_settings.setAttribute('NumFakeFood', str(self.NUM_FF))
        lf_settings.setAttribute('PowerlawFakeFoodUnitCount', str(self.NUM_PLAW_FF))
        lf_settings.setAttribute('NumFakeClusters', str(self.NUM_FCL))
        lf_settings.setAttribute('FakeClusterWidthX', str(self.FCL_X))
        lf_settings.setAttribute('FakeClusterWidthY', str(self.FCL_Y))
        lf_settings.setAttribute('FilenameHeader', str(self.fname_header))
        lf_settings.setAttribute('Densify', str(self.DENSIFY))
        lf_settings.setAttribute('ForagingAreaSize', self.foragingAreaSize())
        lf_settings.setAttribute('BotFwdSpeed', str(self.BOT_FW_SPD))
        lf_settings.setAttribute('EstTravelTimeTolerance', str(self.TTT))
        lf_settings.setAttribute('UseDefenseMethod', str(self.USE_DEF))
        lf_settings.setAttribute('UseReturnBoolean', str(self.USE_DEF_RB))
        lf_settings.setAttribute('UseTrailClustering', str(self.USE_DEF_CL))
        lf_settings.setAttribute('UseClusterGraph', str(self.USE_DEF_CG))
        lf_settings.setAttribute('FeedbackLoopWeight', str(self.FLW))
        lf_settings.setAttribute('StrikeLimit', str(self.STRIKE_LIMIT))
        lf_settings.setAttribute('UseFeedbackEq', str(self.USFB))
        lf_settings.setAttribute('RatioCheckFreq', str(self.RATIO_CHECK_FREQ))
        lf_settings.setAttribute('CheckRatio', str(self.USE_RATIO_CHECK))
        loops.appendChild(lf_settings)
        #       </settings>

        #       <detractor_settings>
        lf_detractor_settings = xml.createElement('detractor_settings')
        lf_detractor_settings.setAttribute("NumAtkNests", str(self.NUM_ATK_NESTS))
        lf_detractor_settings.setAttribute('AtkNest1Position', f'{self.ATK_NEST1_POS[0]:.1f},{self.ATK_NEST1_POS[1]:.1f}')
        lf_detractor_settings.setAttribute('AtkNest2Position', f'{self.ATK_NEST2_POS[0]:.1f},{self.ATK_NEST2_POS[1]:.1f}')
        lf_detractor_settings.setAttribute('AtkNest3Position', f'{self.ATK_NEST3_POS[0]:.1f},{self.ATK_NEST3_POS[1]:.1f}')
        lf_detractor_settings.setAttribute('AtkNest4Position', f'{self.ATK_NEST4_POS[0]:.1f},{self.ATK_NEST4_POS[1]:.1f}')
        lf_detractor_settings.setAttribute('AtkNestRadius', str(self.ATK_NEST_RAD))
        loops.appendChild(lf_detractor_settings)
        #       </detractor_settings>

        #   </loop_functions>

        #   <arena>
        arena = xml.createElement('arena')
        arena.setAttribute('size',self.arenaSize())
        arena.setAttribute('center','0,0,0.5')
        argos_config.appendChild(arena)

        #       <floor>
        floor = xml.createElement('floor')
        floor.setAttribute('id', 'floor')
        floor.setAttribute('pixels_per_meter', '10')
        floor.setAttribute('source', 'loop_functions')
        arena.appendChild(floor)

        #       <box>
        wall_n = xml.createElement('box')
        wall_n.setAttribute('id','wall_north')
        wall_n.setAttribute('size',self.wallSize('north'))
        wall_n.setAttribute('movable','false')
        arena.appendChild(wall_n)

        #           <body>
        body_n = xml.createElement('body')
        body_n.setAttribute('position',self.wallPosition('north'))
        body_n.setAttribute('orientation','0,0,0')
        wall_n.appendChild(body_n)

        #       <box>
        wall_s = xml.createElement('box')
        wall_s.setAttribute('id','wall_south')
        wall_s.setAttribute('size',self.wallSize('south'))
        wall_s.setAttribute('movable','false')
        arena.appendChild(wall_s)

        #           <body>
        body_s = xml.createElement('body')
        body_s.setAttribute('position',self.wallPosition('south'))
        body_s.setAttribute('orientation','0,0,0')
        wall_s.appendChild(body_s)

        #       <box>
        wall_e = xml.createElement('box')
        wall_e.setAttribute('id','wall_east')
        wall_e.setAttribute('size',self.wallSize('east'))
        wall_e.setAttribute('movable','false')
        arena.appendChild(wall_e)

        #           <body>
        body_e = xml.createElement('body')
        body_e.setAttribute('position',self.wallPosition('east'))
        body_e.setAttribute('orientation','0,0,0')
        wall_e.appendChild(body_e)

        #       <box>
        wall_w = xml.createElement('box')
        wall_w.setAttribute('id','wall_west')
        wall_w.setAttribute('size',self.wallSize('west'))
        wall_w.setAttribute('movable','false')
        arena.appendChild(wall_w)

        #           <body>
        body_w = xml.createElement('body')
        body_w.setAttribute('position',self.wallPosition('west'))
        body_w.setAttribute('orientation','0,0,0')
        wall_w.appendChild(body_w)

        if (self.BOT_DEFAULT_DIST):

            layouts = self.genBotLayouts()

            centers = [('1,1,0.0'), ('1,-1,0.0'), ('-1,1,0.0'), ('-1,-1,0.0')]  # Centers for 4 groups
            entity_ids = ['fb0', 'fb1', 'fb2', 'fb3']  # Entity IDs for 4 groups

            # If there are detractors, add their layout information
            if self.D_BOT_COUNT > 0:
                centers.append(('0.0,0.0,0.0'))  # Center for detractors
                entity_ids.append('dt')  # Entity ID for detractors

            # Loop through each group and the detractors
            for i, (center, entity_id) in enumerate(zip(centers, entity_ids)):
                # Create <distribute> element
                distribution = xml.createElement('distribute')
                arena.appendChild(distribution)
                
                # Create <position> element
                position = xml.createElement('position')
                position.setAttribute('center', center)
                position.setAttribute('distances', '0.3,0.3,0.0')
                position.setAttribute('layout', layouts[i][0])
                position.setAttribute('method', 'grid')
                distribution.appendChild(position)
                
                # Create <orientation> element
                orientation = xml.createElement('orientation')
                orientation.setAttribute('method', 'constant')
                orientation.setAttribute('values', '0.0,0.0,0.0')
                distribution.appendChild(orientation)
                
                # Create <entity> element
                entity = xml.createElement('entity')
                entity.setAttribute('quantity', str(layouts[i][1]))
                entity.setAttribute('max_trials', '100')
                distribution.appendChild(entity)
                
                # Create <foot-bot> element
                foot_bot = xml.createElement('foot-bot')
                foot_bot.setAttribute('id', entity_id)
                entity.appendChild(foot_bot)
                
                # Create <controller> element
                controller = xml.createElement('controller')
                controller.setAttribute('config', 'CPFA')
                foot_bot.appendChild(controller)
        
        #   </arena>

        #   <physics_engines>
        physics_eng = xml.createElement('physics_engines')
        argos_config.appendChild(physics_eng)

        #       <dynamics2d>
        dynamics = xml.createElement('dynamics2d')
        dynamics.setAttribute('id','dyn2d')
        physics_eng.appendChild(dynamics)
        #   </physics_engines>

        #   <media>
        media = xml.createElement('media')
        argos_config.appendChild(media)

        #       <led>
        leds = xml.createElement('led')
        leds.setAttribute('id','leds')
        media.appendChild(leds)
        #   </media>

        if (self.VISUAL):
            #   <visualization>
            visualization = xml.createElement('visualization')
            argos_config.appendChild(visualization)

            #       <qt-opengl>
            qt = xml.createElement('qt-opengl')
            visualization.appendChild(qt)

            #           <camera>
            camera = xml.createElement('camera')
            qt.appendChild(camera)

            #               <placements>
            placements = xml.createElement('placements')
            camera.appendChild(placements)

            #                   <placement>
            placement = xml.createElement('placement')
            placement.setAttribute('index','0')
            placement.setAttribute('position','0,0,13')
            placement.setAttribute('look_at','0,0,0')
            placement.setAttribute('up','0,1,0')
            placement.setAttribute('lens_focal_length',str(self.CAM_HEIGHT))
            placements.appendChild(placement)
            #               </placements>
            #           </camera>
            usr_f = xml.createElement('user_functions')
            usr_f.setAttribute('label','CPFA_qt_user_functions')
            qt.appendChild(usr_f)
            #       </qt-opengl>
            #   </visualization>

        # </argos-configuration>

        xml_str = xml.toprettyxml(indent = "\t")

        with open(self.XML_FNAME, "w") as f:
            f.write(xml_str)














# ############## FB group 0 #################
        # #       <distribute>
        #     fb0_distribution = xml.createElement('distribute')
        #     arena.appendChild(fb0_distribution)
        # #           <position>
        #     fb0_position = xml.createElement('position')
        #     fb0_position.setAttribute('center', '1,1,0.0')
        #     fb0_position.setAttribute('distances','0.3,0.3,0.0')
        #     fb0_position.setAttribute('layout',layouts[0][0])
        #     fb0_position.setAttribute('method','grid')
        #     fb0_distribution.appendChild(fb0_position)
        # #           </position

        # #           <orientation>
        #     fb0_orientation = xml.createElement('orientation')
        #     fb0_orientation.setAttribute('method','constant')
        #     fb0_orientation.setAttribute('values','0.0,0.0,0.0')
        #     fb0_distribution.appendChild(fb0_orientation)
        # #           </orientation>

        # #           <entity>
        #     entity0 = xml.createElement('entity')
        #     entity0.setAttribute('quantity', str(layouts[0][1]))
        #     entity0.setAttribute('max_trials','100')
        #     fb0_distribution.appendChild(entity0)

        # #               <foot-bot>
        #     fb0 = xml.createElement('foot-bot')
        #     fb0.setAttribute('id','fb0')
        #     entity0.appendChild(fb0)

        # #                   <controller>
        #     cont_fb0 = xml.createElement('controller')
        #     cont_fb0.setAttribute('config','CPFA')
        #     fb0.appendChild(cont_fb0)
        # #                   </controller>
        # #               </foot-bot>
        # #           </entity>
        # #       </distribute>
        # ############## FB group 1 #################
        # #       <distribute>
        #     fb1_distribution = xml.createElement('distribute')
        #     arena.appendChild(fb1_distribution)
        # #           <position>
        #     fb1_position = xml.createElement('position')
        #     fb1_position.setAttribute('center', '1,-1,0.0')
        #     fb1_position.setAttribute('distances','0.3,0.3,0.0')
        #     fb1_position.setAttribute('layout',layouts[1][0])
        #     fb1_position.setAttribute('method','grid')
        #     fb1_distribution.appendChild(fb1_position)
        # #           </position

        # #           <orientation>
        #     fb1_orientation = xml.createElement('orientation')
        #     fb1_orientation.setAttribute('method','constant')
        #     fb1_orientation.setAttribute('values','0.0,0.0,0.0')
        #     fb1_distribution.appendChild(fb1_orientation)
        # #           </orientation>

        # #           <entity>
        #     entity1 = xml.createElement('entity')
        #     entity1.setAttribute('quantity', str(layouts[1][1]))
        #     entity1.setAttribute('max_trials','100')
        #     fb1_distribution.appendChild(entity1)

        # #               <foot-bot>
        #     fb1 = xml.createElement('foot-bot')
        #     fb1.setAttribute('id','fb1')
        #     entity1.appendChild(fb1)

        # #                   <controller>
        #     cont_fb1 = xml.createElement('controller')
        #     cont_fb1.setAttribute('config','CPFA')
        #     fb1.appendChild(cont_fb1)
        # #                   </controller>
        # #               </foot-bot>
        # #           </entity>
        # ############## FB group 2 #################
        # #       <distribute>
        #     fb2_distribution = xml.createElement('distribute')
        #     arena.appendChild(fb2_distribution)
        # #           <position>
        #     fb2_position = xml.createElement('position')
        #     fb2_position.setAttribute('center', '-1,1,0.0')
        #     fb2_position.setAttribute('distances','0.3,0.3,0.0')
        #     fb2_position.setAttribute('layout',layouts[2][0])
        #     fb2_position.setAttribute('method','grid')
        #     fb2_distribution.appendChild(fb2_position)
        # #           </position

        # #           <orientation>
        #     fb2_orientation = xml.createElement('orientation')
        #     fb2_orientation.setAttribute('method','constant')
        #     fb2_orientation.setAttribute('values','0.0,0.0,0.0')
        #     fb2_distribution.appendChild(fb2_orientation)
        # #           </orientation>

        # #           <entity>
        #     entity2 = xml.createElement('entity')
        #     entity2.setAttribute('quantity', str(layouts[2][1]))
        #     entity2.setAttribute('max_trials','100')
        #     fb2_distribution.appendChild(entity2)

        # #               <foot-bot>
        #     fb2 = xml.createElement('foot-bot')
        #     fb2.setAttribute('id','fb2')
        #     entity2.appendChild(fb2)

        # #                   <controller>
        #     cont_fb2 = xml.createElement('controller')
        #     cont_fb2.setAttribute('config','CPFA')
        #     fb2.appendChild(cont_fb2)
        # #                   </controller>
        # #               </foot-bot>
        # #           </entity>
        # #       </distribute>
        # ############## FB group 3 #################
        # #       <distribute>
        #     fb3_distribution = xml.createElement('distribute')
        #     arena.appendChild(fb3_distribution)
        # #           <position>
        #     fb3_position = xml.createElement('position')
        #     fb3_position.setAttribute('center', '-1,-1,0.0')
        #     fb3_position.setAttribute('distances','0.3,0.3,0.0')
        #     fb3_position.setAttribute('layout',layouts[3][0])
        #     fb3_position.setAttribute('method','grid')
        #     fb3_distribution.appendChild(fb3_position)
        # #           </position

        # #           <orientation>
        #     fb3_orientation = xml.createElement('orientation')
        #     fb3_orientation.setAttribute('method','constant')
        #     fb3_orientation.setAttribute('values','0.0,0.0,0.0')
        #     fb3_distribution.appendChild(fb3_orientation)
        # #           </orientation>

        # #           <entity>
        #     entity3 = xml.createElement('entity')
        #     entity3.setAttribute('quantity', str(layouts[3][1]))
        #     entity3.setAttribute('max_trials','100')
        #     fb3_distribution.appendChild(entity3)

        # #               <foot-bot>
        #     fb3 = xml.createElement('foot-bot')
        #     fb3.setAttribute('id','fb3')
        #     entity3.appendChild(fb3)

        # #                   <controller>
        #     cont_fb3 = xml.createElement('controller')
        #     cont_fb3.setAttribute('config','CPFA')
        #     fb3.appendChild(cont_fb3)
        # #                   </controller>
        # #               </foot-bot>
        # #           </entity>
        # #       </distribute>



        # ################################################
        # ############ DETRACTOR DISTRIBUTION ############
        # ################################################

        # #       <distribute>
        #     dt_distribution = xml.createElement('distribute')
        #     arena.appendChild(dt_distribution)
        # #           <position>
        #     dt_position = xml.createElement('position')
        #     dt_position.setAttribute('center', '0.0,0.0,0.0')
        #     dt_position.setAttribute('distances','0.3,0.3,0.0')
        #     dt_position.setAttribute('layout',layouts[-1][0])
        #     dt_position.setAttribute('method','grid')
        #     dt_distribution.appendChild(dt_position)
        # #           </position

        # #           <orientation>
        #     dt_orientation = xml.createElement('orientation')
        #     dt_orientation.setAttribute('method','constant')
        #     dt_orientation.setAttribute('values','0.0,0.0,0.0')
        #     dt_distribution.appendChild(dt_orientation)
        # #           </orientation>

        # #           <entity>
        #     entity_dt = xml.createElement('entity')
        #     entity_dt.setAttribute('quantity', str(layouts[-1][1]))
        #     entity_dt.setAttribute('max_trials','100')
        #     dt_distribution.appendChild(entity_dt)

        # #               <foot-bot>
        #     dt = xml.createElement('foot-bot')
        #     dt.setAttribute('id','dt')
        #     entity_dt.appendChild(dt)

        # #                   <controller>
        #     cont_dt = xml.createElement('controller')
        #     cont_dt.setAttribute('config','CPFA')
        #     dt.appendChild(cont_dt)
        # #                   </controller>
        # #               </foot-bot>
        # #           </entity>
        # #       </distribute>



        # ################################################
        # ################################################