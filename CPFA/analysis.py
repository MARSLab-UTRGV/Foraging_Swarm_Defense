import xml_config as config
import os, time
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import shutil, sys
import pandas as pd
np.set_printoptions(suppress=True)

SIM_TIME = []
TOTAL_FOOD_COLLECTED = []
TOTAL_COLLECTION_RATE = []
ROBOTS_CAPTURED = []
ROBOT_CAPTURE_RATE = []
REAL_PTRAILS_CREATED = []
FAKE_PTRAILS_CREATED = []
COLLISION_TIME = []
RANDOM_SEED = []
TOTAL_ISOLATED_BOTS = []
NUM_FALSE_POSITIVES = []
TOTAL_ISOLATED_DETRACTORS = []
TOTAL_ISOLATED_FORAGERS = []

def Read(fname):
    count = 0
    SIM_TIME.clear()
    TOTAL_FOOD_COLLECTED.clear()
    TOTAL_COLLECTION_RATE.clear()
    ROBOTS_CAPTURED.clear()
    ROBOT_CAPTURE_RATE.clear()
    REAL_PTRAILS_CREATED.clear()
    FAKE_PTRAILS_CREATED.clear()
    COLLISION_TIME.clear()
    RANDOM_SEED.clear()
    TOTAL_ISOLATED_BOTS.clear()
    NUM_FALSE_POSITIVES.clear()
    TOTAL_ISOLATED_DETRACTORS.clear()
    TOTAL_ISOLATED_FORAGERS.clear()
    
    with open(fname) as f:
        for line in f.readlines():
            data = line.strip().split(',')
            if data[0] == 'Simulation Time (seconds)':
                continue
            SIM_TIME.append(data[0])
            TOTAL_FOOD_COLLECTED.append(data[1])
            TOTAL_COLLECTION_RATE.append(data[2])
            ROBOTS_CAPTURED.append(data[3])
            ROBOT_CAPTURE_RATE.append(data[4])
            REAL_PTRAILS_CREATED.append(data[5])
            FAKE_PTRAILS_CREATED.append(data[6])
            COLLISION_TIME.append(data[7])
            RANDOM_SEED.append(data[8])
            TOTAL_ISOLATED_BOTS.append(data[9])
            NUM_FALSE_POSITIVES.append(data[10])
            TOTAL_ISOLATED_DETRACTORS.append(data[11])
            TOTAL_ISOLATED_FORAGERS.append(data[12])

def GetFoodCollected(flist, rdpath):
    TFClist = []
    Caplist = []

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(float))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(float))

    TFCdata = []
    for r in TFClist:
        TFCdata.append((round(np.mean(r),1),np.std(r)))
    Capdata = []
    for f in Caplist:
        Capdata.append((round(np.mean(f),1),np.std(f)))

    return TFCdata 

def DirectoryExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True

def DirectoryEmpty(path):
    # Check if the directory is empty and return true if so, else false
    if len(os.listdir(path)) == 0:
        return True
    else:
        return False

def ClearDirectory(path):
    # Clear the directory
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

######### TESTING #########

def quickTest():
    
    run_count = 1

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = True
    sim_time = 1800
    XML.MAX_SIM_TIME = sim_time
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.BOT_COUNT = total_robots
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/trash/'
    # XML.INC_MLT = "true"
    XML.LET_DET_USE_MLT = "false"
    XML.DRAW_TRAILS = 1

    XML.XML_FNAME = "./experiments/Misleading_Trail_1.xml"

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    total_food = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    det_percent = 25

    # Set detractors to have a higher rate of laying pheromones
    XML.RLP_F = "4.0"
    XML.RLP_D = "1.0"

    flist = []

    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.USE_DEF_CG = "true"

    XML.setDetractorPercentage(det_percent, True)
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {det_percent}%\n')
        os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp6_percentages(flist, XML.RD_PATH, total_robots, total_food, False)

def visualTest():
    
    run_count = 5

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = True
    XML.Densify(False)
    XML.UseQZone(False)
    XML.UseFFDoS(False)
    XML.UseMisleadingTrailAttack(True)
    XML.setBotCount(32)
    XML.MAX_SIM_TIME = 1800
    XML.setDistribution(1)
    XML.DRAW_TRAILS = 1
    # XML.NUM_DETRACTORS = 4
    XML.NUM_ATK_NESTS = 4

    lambda_list = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]     # Rates of laying pheromone

    XML.setDetractorPercentage(25)
    # XML.RANDOM_SEED = 283291
    XML.RD_PATH=f'results/'
    XML.setFname()
    DirectoryExists(XML.RD_PATH)
    # if not DirectoryEmpty(XML.RD_PATH):
    #     ClearDirectory(XML.RD_PATH)

    # XML.RANDOM_SEED=120678
    # XML.RANDOM_SEED=743490
    # XML.RANDOM_SEED=301421

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    # fname = XML.setFname()+"AttackData.txt"
            
    for p in lambda_list:

        user_input = input(f"Lambda: {p}\n Proceed? (y/n): ")

        if user_input.lower() == "n":
            user_input = input(f"Terminate experiment (skip all)? (y/n): ")
            if user_input.lower() == "n":
                print(f'Continuing to next labmda value...\n')
                continue
            elif user_input.lower() == "y":
                break
            else:
                print("Invalid input. Continuing.")
                pass

        elif user_input.lower() == "y":
            print (f'Proceeding with current lambda value...\n')
            pass
        else:
            print(f"Invalid input. Proceeding with current lambda value...\n.")
            pass

        for i in range(run_count):
            XML.RLP_F = p
            XML.createXML()
            print(f'Lambda: {XML.RLP_F}\n')
            
            # Prompt user for input
            user_input = input(f"{run_count - i} runs left. Continue?  (y/n): ")
            
            # Check if user wants to continue or skip the rest of the loop
            if user_input.lower() == "n":
                print(f'Proceeding to next lambda value...')
                break
            elif user_input.lower() == "y":
                print(f'Proceeding with current lambda value...\n')
                os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
                pass
            else:
                print("Invalid input. Proceeding with current lambda value...")
                pass

def PreExperiment(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Use increased density for fake food
    XML.setBotCount(24)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS = 0
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Standard CPFA, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # w/ Misleading trail attack
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 1
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Standard CPFA, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    print(GetFoodCollected(flist, XML.RD_PATH))

    # PlotExp1(flist, XML.RD_PATH)
    # CheckForTerminatedSimulations(XML.RD_PATH)
    # PlotExp1_merge_test(flist, RFmax, FFmax)

def GetCorrelationMatrix(flist, rdpath):
    # Replace this with your actual CSV file path
    
    for filename in flist:
        # Read the data into a pandas DataFrame
        df = pd.read_csv(filename)

        # Calculate the correlation matrix
        correlation_matrix = df.corr()

        # Print the correlation matrix
        print(correlation_matrix)

######### EXPERIMENT check ratio (attack only) #########
    
def AnalysisExp1(rc):

    # In this experiment, we will be varying the layrate. This is to check the ratio of real to misleading trails along with the foraging performance of the attack alone.
    # We will also prevent the detractors from selecting misleading trails to see how the performance is affected.

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.UseMisleadingTrailAttack(True)
    XML.USE_RATIO_CHECK = "true"
    XML.BOT_COUNT = 24
    XML.setDetractorPercentage(25, True)  # static number of foragers

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "4.0", "8.0", "12.0"]     # Rates of laying pheromone

    XML.RD_PATH=f'results/analysis_12-14-23/results_analysis1_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 1: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    XML.MAX_SIM_TIME = 2700

    XML.RD_PATH=f'results/analysis_12-14-23/results_analysis1_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)
    
    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 2: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    XML.LET_DET_USE_MLT = "false"

    XML.RD_PATH=f'results/analysis_12-14-23/results_analysis1_NotLetDetUseMLT_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 3: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

def AnalysisExp2_NotLetDetUseMLT(rc):

    # In this experiment, we will be varying the layrate. This is to check the ratio of real to misleading trails along with the foraging performance of the attack alone.
    # We will also prevent the detractors from selecting misleading trails to see how the performance is affected.

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.UseMisleadingTrailAttack(True)
    XML.USE_RATIO_CHECK = "true"
    XML.BOT_COUNT = 24
    XML.setDetractorPercentage(25, True)  # static number of foragers
    XML.LET_DET_USE_MLT = "false"


    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "4.0", "8.0", "12.0"]     # Rates of laying pheromone

    XML.RD_PATH=f'results/analysis_12-18-23/results_analysis2_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 1: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

def AnalysisExp3(rc):
    # In this experiment, we will be varying the layrate. This is to check the ratio of real to misleading trails along with the foraging performance of the attack alone.
    # We will also prevent the detractors from selecting misleading trails to see how the performance is affected.

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 32
    XML.setBotCount(robot_count)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.UseMisleadingTrailAttack(False)
    XML.USE_RATIO_CHECK = "true"
    XML.BOT_COUNT = 32
    XML.setDetractorPercentage(0, True)  # static number of foragers
    XML.LET_DET_USE_MLT = "false"


    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "4.0", "8.0", "12.0"]     # Rates of laying pheromone

    XML.RD_PATH=f'results/analysis_12-18-23/results_analysis3_noAtk_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 1: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    XML.RD_PATH=f'results/analysis_12-18-23/results_analysis3_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.setDetractorPercentage(25, True)  # static number of foragers
    XML.UseMisleadingTrailAttack(True)

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 1: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

def AnalysisExp4(rc):
    # In this experiment, we will be varying the layrate. This is to check the ratio of real to misleading trails along with the foraging performance of the attack alone.
    # We will also prevent the detractors from selecting misleading trails to see how the performance is affected.

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 32
    XML.setBotCount(robot_count)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.UseMisleadingTrailAttack(False)
    XML.USE_RATIO_CHECK = "true"
    XML.BOT_COUNT = 32
    XML.setDetractorPercentage(0, True)  # static number of foragers
    XML.LET_DET_USE_MLT = "false"


    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "4.0", "8.0", "12.0"]     # Rates of laying pheromone

    XML.RD_PATH=f'results/analysis_12-21-23/results_analysis4_r{robot_count}_{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.setDetractorPercentage(25, True)  # static number of foragers
    XML.UseMisleadingTrailAttack(True)

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    for p in lambda_list:
        XML.RLP_F = p
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack 1: Iteration: {j+1}/{run_count}, Sim Time: {XML.MAX_SIM_TIME}, Lay Rate: {p}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

if __name__ == "__main__":

    # AnalysisExp1(30)
    # AnalysisExp2_NotLetDetUseMLT(30)
    # AnalysisExp3(30)
    # AnalysisExp4(30)
    quickTest()


















    # os.system("./build.sh")

    # quickTest()
    # Experiment1(30)
    # Experiment1_replot(30)
    # visualTest()
    # Experiment2(30)
    # Experiment2_replot(30)
    # Experiment3(30)

    #### uncomment to print results for pre experiment (be sure to comment out above code to avoid running experiments) ####

        # rd_path=f'results/results_PreExp_{30}it/'
        # flist = []
        # flist.append("./results/results_PreExp_30it/CPFA_density-std_R-cl_F-cl_r24_d0_rfc108_10by10_time900_iter30_AttackData.txt")
        # flist.append("./results/results_PreExp_30it/CPFA_density-std_R-cl_F-cl_r24_d1_rfc108_10by10_time900_iter30_AttackData.txt")
        # print(GetFoodCollected(flist, rd_path))

        #### format: <cpfa_std(total food collected, std deviation)>, <cpfa_attacked(total food collected, std deviation)> ####
















#################################################################################
############################# OLD EXPERIMENTS ###################################
#################################################################################

######### EXPERIMENT 1 #########

#TODO: Experiment1 does not account for new code with multiple attacker nests. Need to update the experiment parameters if we want to rerun this experiment.

def Old_PlotExp1(flist, rdpath):

    TFClist = []
    Caplist = []

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(float))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(float))

    # print(TFClist)
    # print(Caplist)
    
    TFCdata = []
    for r in TFClist:
        TFCdata.append((round(np.mean(r),1),np.std(r)))
    Capdata = []
    for f in Caplist:
        Capdata.append((round(np.mean(f),1),np.std(f)))

    # print(TFCdata)
    # print(Capdata)

    x_tick_labels = ['0','1','2','3','4']

    # Extracting mean and standard deviation
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Number of detractors (0 to 4)
    detractors = np.arange(0, 5)

    # Line Plot
    # fig, ax1 = plt.subplots()
    fig, axs = plt.subplots(2,1,figsize=(10,10), sharex=False)


    # Twin the axes for two different y-axes.
    # ax2 = ax1.twinx()

    # Plot the data
    # ax1.errorbar(detractors, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='b')
    # ax2.errorbar(detractors, robot_captured_mean, yerr=robot_captured_stdev, fmt='x-', label='Robots Captured', color='r')
    axs[0].errorbar(detractors, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='b', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_title('Food Collection vs. Number of Detractors')
    axs[0].set_xlabel('Number of Detractors')
    axs[0].set_ylabel('Food Collected')
    axs[0].grid(True)

    axs[1].errorbar(detractors, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='r', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_title('Robots Captured vs. Number of Detractors')
    axs[1].set_xlabel('Number of Detractors')
    axs[1].set_ylabel('Robots Captured')
    axs[1].grid(True)
    # axs[1].xaxis.tick_top()


    # axs[0].set_ylim(70, 110)
    # axs[1].set_ylim(0, 10)

    axs[0].set_xticks(detractors, x_tick_labels)
    axs[1].set_xticks(detractors, x_tick_labels)

    # plt.title('Impact of Number of Detractors')
    # plt.show()

    plt.tight_layout()

    plt.savefig(f'{rdpath}Experiment1_lineplot.png')

    plt.clf()


    # # Bar Plot
    # fig, ax = plt.subplots(nrows=2)

    # labelsize = 14
    # textsize = 23
    # top_plt_pad = -125
    # bottom_plt_pad = -25
    # top_labelcolor = 'white'
    # bottom_labelcolor = 'black'
    # bar_zorder = 0
    # label_zorder = 15
    # b_label_rotation = 30
    # width=0.23
    # multiplier=0
    # x = np.arange(len(x_tick_labels))


    # offset = width * multiplier
    # rect1 = ax[0].bar(x+offset, food_collection_mean, width, align="center", yerr=food_collection_stdev, ecolor='orange', label='$FA_{std}$', edgecolor='black', color='blue', zorder=bar_zorder)
    # ax[0].bar_label(rect1,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # multiplier+=1

    # offset = width * multiplier
    # rect2 = ax[0].bar(x+offset, robot_captured_mean, width, align="center", yerr=robot_captured_stdev, ecolor='orange', label='$FA_{atk}$', edgecolor='black', color='green', zorder=bar_zorder)
    # ax[0].bar_label(rect2,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # multiplier+=1

    # handles1, labels1 = ax[0].get_legend_handles_labels()
    # plt.legend(handles1, labels1, loc='lower left', ncol=2, fontsize=textsize)

    # # ax[0].set_ylim(0,maxRealFood)
    # ax[0].set_ylabel('Resources Collected', fontsize=textsize)
    # # ax[1].set_ylim(0,85)
    # ax[1].set_ylabel('Robots Captured', fontsize=textsize, labelpad = 11)
    # ax[1].invert_yaxis()

    # ax[1].set_xticks(x+width, x_tick_labels, fontsize=labelsize)
    # ax[1].xaxis.tick_bottom()
    # ax[1].set_xlabel('Number of Detractors', fontsize=textsize)

    # # ax[0].set_title('Foraging Results by Maximum Simulation Time')

    # fig.tight_layout()
    # fig.subplots_adjust(hspace=0)

    # # plt.savefig('results/Experiment_2.png')
    # plt.savefig(f'{rdpath}/Experiment1_boxplot.png')

def Old_Experiment1(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Use increased density for fake food
    XML.setBotCount(12)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_{run_count}it_r12/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS = 0
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Standard CPFA, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # w/ Misleading trail attack w/ 1 detractor
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 1
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Misleading Trail Attack, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
    
    # w/ Misleading trail attack w/ 2 detractors
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 2
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Misleading Trail Attack, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
    
    # w/ Misleading trail attack w/ 3 detractors
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 3
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Misleading Trail Attack, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # w/ Misleading trail attack w/ 4 detractors
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 4
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Misleading Trail Attack, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Detractors: {XML.NUM_DETRACTORS}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp1(flist, XML.RD_PATH)

def Old_Experiment1_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Use increased density for fake food
    XML.setBotCount(24)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS = 0
    flist.append(XML.setFname()+"AttackData.txt")

    # w/ Misleading trail attack w/ 1 detractor
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 1
    flist.append(XML.setFname()+"AttackData.txt")
    
    # w/ Misleading trail attack w/ 2 detractors
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 2
    flist.append(XML.setFname()+"AttackData.txt")
    
    # w/ Misleading trail attack w/ 3 detractors
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 3
    flist.append(XML.setFname()+"AttackData.txt")

    # w/ Misleading trail attack w/ 4 detractors
    XML.UseMisleadingTrailAttack(True) 
    XML.NUM_DETRACTORS = 4
    flist.append(XML.setFname()+"AttackData.txt")
   
    PlotExp1(flist, XML.RD_PATH)

######### EXPERIMENT 2 #########

def Old_Experiment2(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    XML.setBotCount(32)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp2_{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS_NEST1 = 0
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 0
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Standard CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # CPFA Misleading Trail Attack (1 nest, 4 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 1
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
    
    # CPFA Misleading Trail Attack (2 nests, 8 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 2
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
    
    # CPFA Misleading Trail Attack (3 nests, 12 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 4
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 3
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # CPFA Misleading Trail Attack (4 nests, 16 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 4
    XML.NUM_DETRACTORS_NEST4 = 4
    XML.NUM_ATK_NESTS = 4
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

def Old_PlotExp2(flist, rdpath):

    TFClist = []
    Caplist = []

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(float))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(float))

    # print(TFClist)
    # print(Caplist)
    
    TFCdata = []
    for r in TFClist:
        TFCdata.append((round(np.mean(r),1),np.std(r)))
    Capdata = []
    for f in Caplist:
        Capdata.append((round(np.mean(f),1),np.std(f)))

    # print(TFCdata)
    # print(Capdata)

    x_tick_labels = ['0','1','2','3','4']

    # Extracting mean and standard deviation
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Number of detractors (0 to 4)
    detractors = np.arange(0, 5)

    # Line Plot
    fig, axs = plt.subplots(2,1,figsize=(10,10), sharex=False)

    # Plot the data
    axs[0].errorbar(detractors, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='b', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_title('Food Collection vs. Number of Attack Nests')
    axs[0].set_xlabel('Number of Attack Nests (4 Detractors per Nest)')
    axs[0].set_ylabel('Food Collected')
    axs[0].grid(True)

    axs[1].errorbar(detractors, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='r', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_title('Robots Captured vs. Number of Attack Nests')
    axs[1].set_xlabel('Number of Attack Nests (4 Detractors per Nest)')
    axs[1].set_ylabel('Robots Captured')
    axs[1].grid(True)

    axs[0].set_xticks(detractors, x_tick_labels)
    axs[1].set_xticks(detractors, x_tick_labels)

    plt.tight_layout()

    plt.savefig(f'{rdpath}Experiment2_lineplot.png')

    plt.clf()

def Old_Experiment2_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    XML.setBotCount(32)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp2_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS_NEST1 = 0
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 0
    flist.append(XML.setFname()+"AttackData.txt")

    # CPFA Misleading Trail Attack (1 nest, 4 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 1
    flist.append(XML.setFname()+"AttackData.txt")
   
    # CPFA Misleading Trail Attack (2 nests, 8 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 2
    flist.append(XML.setFname()+"AttackData.txt")
    
    # CPFA Misleading Trail Attack (3 nests, 12 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 4
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 3
    flist.append(XML.setFname()+"AttackData.txt")
    
    # CPFA Misleading Trail Attack (4 nests, 16 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 4
    XML.NUM_DETRACTORS_NEST4 = 4
    XML.NUM_ATK_NESTS = 4
    flist.append(XML.setFname()+"AttackData.txt")

    PlotExp2(flist, XML.RD_PATH)

######### EXPERIMENT 3 #########

def Old_Experiment3(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    XML.setBotCount(32)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp3_{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS_NEST1 = 0
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 0
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Standard CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # CPFA Misleading Trail Attack (1 nest, 4 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 1
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 1
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
    
    # CPFA Misleading Trail Attack (2 nests, 8 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 1
    XML.NUM_DETRACTORS_NEST2 = 1
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 2
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")
    
    # CPFA Misleading Trail Attack (3 nests, 12 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 1
    XML.NUM_DETRACTORS_NEST2 = 1
    XML.NUM_DETRACTORS_NEST3 = 1
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 3
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # CPFA Misleading Trail Attack (4 nests, 16 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 1
    XML.NUM_DETRACTORS_NEST2 = 1
    XML.NUM_DETRACTORS_NEST3 = 1
    XML.NUM_DETRACTORS_NEST4 = 1
    XML.NUM_ATK_NESTS = 4
    flist.append(XML.setFname()+"AttackData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Attacked CPFA, Iteration: {j+1}, Num Resources: {XML.NUM_RF}, Num Atk Nests: {XML.NUM_ATK_NESTS}, Num Detractors: {XML.getNumDetractors()}\n')
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp3(flist, XML.RD_PATH)

def Old_PlotExp3(flist, rdpath):

    TFClist = []
    Caplist = []

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(float))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(float))

    # print(TFClist)
    # print(Caplist)
    
    TFCdata = []
    for r in TFClist:
        TFCdata.append((round(np.mean(r),1),np.std(r)))
    Capdata = []
    for f in Caplist:
        Capdata.append((round(np.mean(f),1),np.std(f)))

    # print(TFCdata)
    # print(Capdata)

    x_tick_labels = ['0','1','2','3','4']

    # Extracting mean and standard deviation
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Number of detractors (0 to 4)
    detractors = np.arange(0, 5)

    # Line Plot
    fig, axs = plt.subplots(2,1,figsize=(10,10), sharex=False)

    # Plot the data
    axs[0].errorbar(detractors, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='b', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_title('Food Collection vs. Number of Attack Nests')
    axs[0].set_xlabel('Number of Attack Nests (4 Detractors per Nest)')
    axs[0].set_ylabel('Food Collected')
    axs[0].grid(True)

    axs[1].errorbar(detractors, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='r', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_title('Robots Captured vs. Number of Attack Nests')
    axs[1].set_xlabel('Number of Attack Nests (4 Detractors per Nest)')
    axs[1].set_ylabel('Robots Captured')
    axs[1].grid(True)

    axs[0].set_xticks(detractors, x_tick_labels)
    axs[1].set_xticks(detractors, x_tick_labels)

    plt.tight_layout()

    plt.savefig(f'{rdpath}Experiment2_lineplot.png')

    plt.clf()

def Old_Experiment3_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    XML.setBotCount(32)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp2_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    flist = []

    # Standard CPFA
    XML.UseMisleadingTrailAttack(False) # Begin with normal runs
    XML.NUM_DETRACTORS_NEST1 = 0
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 0
    flist.append(XML.setFname()+"AttackData.txt")

    # CPFA Misleading Trail Attack (1 nest, 4 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 0
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 1
    flist.append(XML.setFname()+"AttackData.txt")
   
    # CPFA Misleading Trail Attack (2 nests, 8 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 0
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 2
    flist.append(XML.setFname()+"AttackData.txt")
    
    # CPFA Misleading Trail Attack (3 nests, 12 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 4
    XML.NUM_DETRACTORS_NEST4 = 0
    XML.NUM_ATK_NESTS = 3
    flist.append(XML.setFname()+"AttackData.txt")
    
    # CPFA Misleading Trail Attack (4 nests, 16 detractors)
    XML.UseMisleadingTrailAttack(True)
    XML.NUM_DETRACTORS_NEST1 = 4
    XML.NUM_DETRACTORS_NEST2 = 4
    XML.NUM_DETRACTORS_NEST3 = 4
    XML.NUM_DETRACTORS_NEST4 = 4
    XML.NUM_ATK_NESTS = 4
    flist.append(XML.setFname()+"AttackData.txt")

    PlotExp2(flist, XML.RD_PATH)
