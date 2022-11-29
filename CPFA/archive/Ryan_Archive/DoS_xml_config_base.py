from xml.dom import minidom
import math

# import random
# import numpy as np

####### GLOBAL CONSTANTS (DON'T MODIFY) #######

H_C = 0.288699733

####### EVOLVABLE PARAMETERS (DON'T MODIFY) #######

PFS = "1"                           # Print Final Score
# PRN = "0.0147598869881"             # Probability Of Returning To Nest
# PSS = "0.723128706375"              # Probability Of Switching To Searching
# RISD = "0.205799848158"             # Rate Of Informed Search Decay
# RLP = "14.7027566005"               # Rate of Laying Pheromone
# RPD = "0.0245057227138"             # Rate Of Pheromone Decay
# RSF = "14.1514206414"               # Rate Of Site Fidelity
# USV = "2.81939731297"               # Uninformed Search Variation

# Cluster CPFA 10x10 from /experiments/15mins/Cluster_CPFA_10by10.xml

PSS     = "0.3637176255"
PRN     = "0.00297618325581"
USV     = "2.67338576954"
RISD    = "0.253110502082"
RSF     = "1.42036207003"
RLP     = "8.98846470854"
RPD     = "0.063119269938"


####### CONFIGURATION #######

BOT_DEFAULT_DIST =  True                    # Use default distribution found in original CPFA tests
                                            # If this method is used, BOT_COUNT is ignored and 24 bots
                                            # will be used instead in grid distribution mode

# NOT YET IMPLEMENTED
BOT_COUNT =         20                      # total bot count
BOT_DIST_RAD =      1.5                     # Bot distribution radius (uniform distribution in central area)

ARENA_SIZE =        (10,10,1)               # (x,y,z)

# Visualization Settings
CAM_HEIGHT =        35                      # simulation camera height
VISUAL =            True                    # turn on/off visual simulator

# General Config
THREAD_COUNT =      0
SIM_LENGTH =        6000                    # length of experiment in seconds
RANDOM_SEED =       0
TPS =               16                      # ticks/steps per second

# Controller Sensor Settings
SHOW_PROX_RAYS =    "true"                  # turn on/off footbot proximity sensor rays

# Contoller Parameter Settings 
DN_SD =             0.00                    # Destination Noise Standard Deviation
FDT =               0.13                    # Food Distance Tolerance
NAT =               0.10                    # Nest Angle Tolerance
NDT =               0.05                    # Nest Distance Tolerance
PN_SD =             0.00                    # Position Noise Standard Deviation
RD_PATH =           "results/"              # results directory path
BOT_FW_SPD =        16.00                   # robot forward speed
BOT_ROT_SPD =       8.00                    # robot rotation speed
SSS =               0.08                    # Search Step Size
TAT =               0.10                    # Target Angle Tolerance
TDT =               0.05                    # Target Distance Tolerance

# Fake Food Loop Function Settings **
USE_FF_DOS =        "true"                  # Turn on/off fake_food DoS
FFD =               1                       # Fake Food Distribution Mode (0=Random, 1=Cluster, 2=PowerLaw)
NUM_FF =            256                      # Number of fake food to distribute for random distribution
NUM_FCL =           2                       # Number of fake food clusters for cluster distribution
FCL_X =             8                       # Fake cluster width X for cluster distribution
FCL_Y =             8                       # Fake cluster width Y for cluster distribution
NUM_PLAW_FF =       128                     # Number of fake food to distribute for power law distribution

# Real Food Loop Function Settings
RFD =               1                       # Real Food Distribution Mode (0=Random, 1=Cluster, 2=PowerLaw)
NUM_RF =            256                      # Number of real food to distribute for random distribution
NUM_RCL =           4                       # Number of real food clusters for cluster distribution
RCL_X =             8                       # Real cluster width X for cluster distribution
RCL_Y =             8                       # Real cluster width Y for cluster distribution
NUM_PLAW_RF =       256                     # Number of real food to distribute for power law distribution

# Other Loop Function Settings
DRAW_ID =           1                       # Draw bot IDs
DRAW_TARGET_RAYS =  0                       # Draw directional rays to target (for each bot)
DRAW_TRAILS =       0                       # Draw pheromone trails
DRAW_DENSITY_RATE = 4                       # Draw density rate of resources
MAX_SIM_COUNT =     1                       # Max simulation counter
MAX_SIM_TIME =      1800                    # Max simulation time in seconds
OUTPUT_DATA =       0                       # turn output data on/off
NEST_ELV =          0.001                   # Nest elevation
NEST_POS =          (0,0)                   # Nest location
NEST_RAD =          0.25                    # Nest radius
VFP =               0                       # Variable food placement
FOOD_RAD =          0.05                    # Food radius

############################################################


# generates arena size string for xml based on ARENA_SIZE
def arenaSize():
    return str(ARENA_SIZE[0])+','+str(ARENA_SIZE[1])+','+str(ARENA_SIZE[2])

# generates wall size string for each wall face based on ARENA_SIZE
def wallSize(face):
    if (face.lower() == 'north' or face.lower() == 'south'):
        return str(ARENA_SIZE[0])+',0.1,0.5'
    elif (face.lower() == 'east' or face.lower() == 'west'):
        return '0.1,'+str(ARENA_SIZE[1])+',0.5'
    else:
        raise Exception("ERROR: A valid wall name was not given...")

# generates wall position string for each wall face based on ARENA_SIZE
def wallPosition(face):
    if face.lower() == 'north':
        return '0,'+str(ARENA_SIZE[0]/2)+',0'
    elif face.lower() == 'south':
        return '0,-'+str(ARENA_SIZE[0]/2)+',0'
    elif face.lower() == 'east':
        return str(ARENA_SIZE[1]/2)+',0,0'
    elif face.lower() == 'west':
        return '-'+str(ARENA_SIZE[1]/2)+',0,0'
    else:
        raise Exception("ERROR: A valid wall name was not given...")

# for uniform distribution method based on ARENA_SIZE
def botUPosition(limit):
    if limit.lower() == 'min':
        return str(-ARENA_SIZE[0]/2)+','+str(-ARENA_SIZE[1]/2)+',0'
    elif limit.lower() == 'max':
        return str(ARENA_SIZE[0]/2)+','+str(ARENA_SIZE[1]/2)+',0'
    else:
        raise Exception("ERROR: limit name unidentified for botUPosition()")

def createXML():

    xml = minidom.Document()

    # <argos-configuration>
    argos_config = xml.createElement('argos-configuration')
    xml.appendChild(argos_config)

    #   <framework>
    framework = xml.createElement('framework')
    argos_config.appendChild(framework)

    #       <system>
    system = xml.createElement('system')
    system.setAttribute('threads', str(THREAD_COUNT))
    framework.appendChild(system)
    #       <experiment>
    experiment = xml.createElement('experiment')
    experiment.setAttribute('length', str(SIM_LENGTH))
    experiment.setAttribute('ticks_per_second',str(TPS))
    experiment.setAttribute('random_seed', str(RANDOM_SEED))
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
    fb_prox.setAttribute('show_rays',str(SHOW_PROX_RAYS))
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
    params_settings.setAttribute('DestinationNoiseStdev', str(DN_SD))
    params_settings.setAttribute('FoodDistanceTolerance', str(FDT))
    params_settings.setAttribute('NestAngleTolerance', str(NAT))
    params_settings.setAttribute('NestDistanceTolerance', str(NDT))
    params_settings.setAttribute('PositionNoiseStdev', str(PN_SD))
    params_settings.setAttribute('ResultsDirectoryPath', RD_PATH)
    params_settings.setAttribute('RobotForwardSpeed', str(BOT_FW_SPD))
    params_settings.setAttribute('RobotRotationSpeed', str(BOT_ROT_SPD))
    params_settings.setAttribute('SearchStepSize', str(SSS))
    params_settings.setAttribute('TargetAngleTolerance', str(TAT))
    params_settings.setAttribute('TargetDistanceTolerance', str(TDT))
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
    lf_cpfa.setAttribute('PrintFinalScore', str(PFS))
    lf_cpfa.setAttribute('ProbabilityOfReturningToNest', str(PRN))
    lf_cpfa.setAttribute('ProbabilityOfSwitchingToSearching', str(PSS))
    lf_cpfa.setAttribute('RateOfInformedSearchDecay', str(RISD))
    lf_cpfa.setAttribute('RateOfLayingPheromone', str(RLP))
    lf_cpfa.setAttribute('RateOfPheromoneDecay', str(RPD))
    lf_cpfa.setAttribute('RateOfSiteFidelity', str(RSF))
    lf_cpfa.setAttribute('UninformedSearchVariation', str(USV))
    loops.appendChild(lf_cpfa)

    #       <settings>
    lf_settings = xml.createElement('settings')
    lf_settings.setAttribute('DrawIDs', str(DRAW_ID))
    lf_settings.setAttribute('DrawTargetRays', str(DRAW_TARGET_RAYS))
    lf_settings.setAttribute('DrawTrails', str(DRAW_TRAILS))
    lf_settings.setAttribute('DrawDensityRate', str(DRAW_DENSITY_RATE))
    lf_settings.setAttribute('MaxSimCounter', str(MAX_SIM_COUNT))
    lf_settings.setAttribute('MaxSimTimeInSeconds', str(MAX_SIM_TIME))
    lf_settings.setAttribute('OutputData', str(OUTPUT_DATA))
    lf_settings.setAttribute('NestElevation', str(NEST_ELV))
    lf_settings.setAttribute('NestPosition', str(NEST_POS))
    lf_settings.setAttribute('NestRadius', str(NEST_RAD))
    lf_settings.setAttribute('VariableFoodPlacement', str(VFP))
    lf_settings.setAttribute('FoodRadius', str(FOOD_RAD))
    lf_settings.setAttribute('FoodDistribution', str(RFD))
    lf_settings.setAttribute('NumRealFood', str(NUM_RF))
    lf_settings.setAttribute('PowerlawFoodUnitCount', str(NUM_PLAW_RF))
    lf_settings.setAttribute('NumberOfClusters', str(NUM_RCL))
    lf_settings.setAttribute('ClusterWidthX', str(RCL_X))
    lf_settings.setAttribute('ClusterWidthY', str(RCL_Y))
    lf_settings.setAttribute('UseFakeFoodDoS', str(USE_FF_DOS))
    lf_settings.setAttribute('FakeFoodDistribution', str(FFD))
    lf_settings.setAttribute('NumFakeFood', str(NUM_FF))
    lf_settings.setAttribute('PowerlawFakeFoodUnitCount', str(NUM_PLAW_FF))
    lf_settings.setAttribute('NumFakeClusters', str(NUM_FCL))
    lf_settings.setAttribute('FakeClusterWidthX', str(FCL_X))
    lf_settings.setAttribute('FakeClusterWidthY', str(FCL_Y))
    loops.appendChild(lf_settings)
    #       </settings>
    #   </loop_functions>

    #   <arena>
    arena = xml.createElement('arena')
    arena.setAttribute('size',arenaSize())
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
    wall_n.setAttribute('size',wallSize('north'))
    wall_n.setAttribute('movable','false')
    arena.appendChild(wall_n)

    #           <body>
    body_n = xml.createElement('body')
    body_n.setAttribute('position',wallPosition('north'))
    body_n.setAttribute('orientation','0,0,0')
    wall_n.appendChild(body_n)

    #       <box>
    wall_s = xml.createElement('box')
    wall_s.setAttribute('id','wall_south')
    wall_s.setAttribute('size',wallSize('south'))
    wall_s.setAttribute('movable','false')
    arena.appendChild(wall_s)

    #           <body>
    body_s = xml.createElement('body')
    body_s.setAttribute('position',wallPosition('south'))
    body_s.setAttribute('orientation','0,0,0')
    wall_s.appendChild(body_s)

    #       <box>
    wall_e = xml.createElement('box')
    wall_e.setAttribute('id','wall_east')
    wall_e.setAttribute('size',wallSize('east'))
    wall_e.setAttribute('movable','false')
    arena.appendChild(wall_e)

    #           <body>
    body_e = xml.createElement('body')
    body_e.setAttribute('position',wallPosition('east'))
    body_e.setAttribute('orientation','0,0,0')
    wall_e.appendChild(body_e)

    #       <box>
    wall_w = xml.createElement('box')
    wall_w.setAttribute('id','wall_west')
    wall_w.setAttribute('size',wallSize('west'))
    wall_w.setAttribute('movable','false')
    arena.appendChild(wall_w)

    #           <body>
    body_w = xml.createElement('body')
    body_w.setAttribute('position',wallPosition('west'))
    body_w.setAttribute('orientation','0,0,0')
    wall_w.appendChild(body_w)

    if (BOT_DEFAULT_DIST):
    
    ############## FB group 0 #################
    #       <distribute>
        fb0_distribution = xml.createElement('distribute')
        arena.appendChild(fb0_distribution)
    #           <position>
        fb0_position = xml.createElement('position')
        fb0_position.setAttribute('center', '1,1,0.0')
        fb0_position.setAttribute('distances','0.3,0.3,0.0')
        fb0_position.setAttribute('layout','2,3,1')
        fb0_position.setAttribute('method','grid')
        fb0_distribution.appendChild(fb0_position)
    #           </position

    #           <orientation>
        fb0_orientation = xml.createElement('orientation')
        fb0_orientation.setAttribute('method','constant')
        fb0_orientation.setAttribute('values','0.0,0.0,0.0')
        fb0_distribution.appendChild(fb0_orientation)
    #           </orientation>

    #           <entity>
        entity0 = xml.createElement('entity')
        entity0.setAttribute('quantity', '6')
        entity0.setAttribute('max_trials','100')
        fb0_distribution.appendChild(entity0)

    #               <foot-bot>
        fb0 = xml.createElement('foot-bot')
        fb0.setAttribute('id','fb0')
        entity0.appendChild(fb0)

    #                   <controller>
        cont_fb0 = xml.createElement('controller')
        cont_fb0.setAttribute('config','CPFA')
        fb0.appendChild(cont_fb0)
    #                   </controller>
    #               </foot-bot>
    #           </entity>
    #       </distribute>
    ############## FB group 1 #################
    #       <distribute>
        fb1_distribution = xml.createElement('distribute')
        arena.appendChild(fb1_distribution)
    #           <position>
        fb1_position = xml.createElement('position')
        fb1_position.setAttribute('center', '1,-1,0.0')
        fb1_position.setAttribute('distances','0.3,0.3,0.0')
        fb1_position.setAttribute('layout','2,3,1')
        fb1_position.setAttribute('method','grid')
        fb1_distribution.appendChild(fb1_position)
    #           </position

    #           <orientation>
        fb1_orientation = xml.createElement('orientation')
        fb1_orientation.setAttribute('method','constant')
        fb1_orientation.setAttribute('values','0.0,0.0,0.0')
        fb1_distribution.appendChild(fb1_orientation)
    #           </orientation>

    #           <entity>
        entity1 = xml.createElement('entity')
        entity1.setAttribute('quantity', '6')
        entity1.setAttribute('max_trials','100')
        fb1_distribution.appendChild(entity1)

    #               <foot-bot>
        fb1 = xml.createElement('foot-bot')
        fb1.setAttribute('id','fb1')
        entity1.appendChild(fb1)

    #                   <controller>
        cont_fb1 = xml.createElement('controller')
        cont_fb1.setAttribute('config','CPFA')
        fb1.appendChild(cont_fb1)
    #                   </controller>
    #               </foot-bot>
    #           </entity>
    ############## FB group 2 #################
    #       <distribute>
        fb2_distribution = xml.createElement('distribute')
        arena.appendChild(fb2_distribution)
    #           <position>
        fb2_position = xml.createElement('position')
        fb2_position.setAttribute('center', '-1,1,0.0')
        fb2_position.setAttribute('distances','0.3,0.3,0.0')
        fb2_position.setAttribute('layout','2,3,1')
        fb2_position.setAttribute('method','grid')
        fb2_distribution.appendChild(fb2_position)
    #           </position

    #           <orientation>
        fb2_orientation = xml.createElement('orientation')
        fb2_orientation.setAttribute('method','constant')
        fb2_orientation.setAttribute('values','0.0,0.0,0.0')
        fb2_distribution.appendChild(fb2_orientation)
    #           </orientation>

    #           <entity>
        entity2 = xml.createElement('entity')
        entity2.setAttribute('quantity', '6')
        entity2.setAttribute('max_trials','100')
        fb2_distribution.appendChild(entity2)

    #               <foot-bot>
        fb2 = xml.createElement('foot-bot')
        fb2.setAttribute('id','fb2')
        entity2.appendChild(fb2)

    #                   <controller>
        cont_fb2 = xml.createElement('controller')
        cont_fb2.setAttribute('config','CPFA')
        fb2.appendChild(cont_fb2)
    #                   </controller>
    #               </foot-bot>
    #           </entity>
    ############## FB group 3 #################
    #       <distribute>
        fb3_distribution = xml.createElement('distribute')
        arena.appendChild(fb3_distribution)
    #           <position>
        fb3_position = xml.createElement('position')
        fb3_position.setAttribute('center', '-1,-1,0.0')
        fb3_position.setAttribute('distances','0.3,0.3,0.0')
        fb3_position.setAttribute('layout','2,3,1')
        fb3_position.setAttribute('method','grid')
        fb3_distribution.appendChild(fb3_position)
    #           </position

    #           <orientation>
        fb3_orientation = xml.createElement('orientation')
        fb3_orientation.setAttribute('method','constant')
        fb3_orientation.setAttribute('values','0.0,0.0,0.0')
        fb3_distribution.appendChild(fb3_orientation)
    #           </orientation>

    #           <entity>
        entity3 = xml.createElement('entity')
        entity3.setAttribute('quantity', '6')
        entity3.setAttribute('max_trials','100')
        fb3_distribution.appendChild(entity3)

    #               <foot-bot>
        fb3 = xml.createElement('foot-bot')
        fb3.setAttribute('id','fb3')
        entity3.appendChild(fb3)

    #                   <controller>
        cont_fb3 = xml.createElement('controller')
        cont_fb3.setAttribute('config','CPFA')
        fb3.appendChild(cont_fb3)
    #                   </controller>
    #               </foot-bot>
    #           </entity>
    #       </distribute>
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


    if (VISUAL):
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
        placement.setAttribute('up','1,0,0')
        placement.setAttribute('lens_focal_length',str(CAM_HEIGHT))
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

    xml_filename = "./experiments/CPFA_DoS_Simulation.xml"

    with open(xml_filename, "w") as f:
        f.write(xml_str)
