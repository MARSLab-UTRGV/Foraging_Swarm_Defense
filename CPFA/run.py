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
FORAGER_FOOD_COLLECTED = []
DETRACTOR_FOOD_COLLECTED = []

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
    FORAGER_FOOD_COLLECTED.clear()
    DETRACTOR_FOOD_COLLECTED.clear()
    
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
    XML.MAX_SIM_TIME = sim_time     # increased from 1800 to 2700 (+50%)
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.BOT_COUNT = total_robots
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.DRAW_TRAILS = 1
    XML.RD_PATH=f'results/trash'
    # XML.INC_MLT = "true"
    XML.LET_DET_USE_MLT = "false"

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

    percent_list = [30]     # Percentage of detractors

    # Set detractors to have a higher rate of laying pheromones
    XML.RLP_F = "4.0"
    XML.RLP_D = "1.0"

    flist = []

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    for p in percent_list:
        XML.setDetractorPercentage(p, True)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')


    # fname = XML.setFname()+"AttackData.txt"

    for i in range(run_count):
        XML.RLP_F = "4.0"
        # XML.FLW = 0.5
        XML.USE_DEF = "false"
        XML.USE_DEF_CL = "false"
        XML.USE_DEF_CG = "false"
        XML.STRIKE_LIMIT = 5            # strike limit
        XML.TTT = 0.1                   # tolerance
        XML.createXML()
        os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

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

######### EXPERIMENT 1 #########

def Experiment1(rc):

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    sim_time = 2700
    XML.MAX_SIM_TIME = sim_time     # increased from 1800 to 2700 (+50%)
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_r24_st{sim_time}_{run_count}it/'

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

    percent_list = [0, 10, 20, 30, 40, 50]     # Percentage of detractors

    XML.RLP_F = "4.0"     # Experiment 3: rate = 4.0 has most robots captured

    flist = []

    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.USE_DEF_CG = "true"

    for p in percent_list:
        XML.setDetractorPercentage(p)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp1_percentages(flist, XML.RD_PATH, total_robots, total_food)

def Experiment1_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 2700
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(0) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_noDef_r24_st2700_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    percent_list = [10, 20, 30, 40, 50]
    XML.RLP_F = "4.0"
    flist = []

    flist.append(XML.setFname()+"AttackData.txt")

    for p in percent_list:

        XML.setDetractorPercentage(p)
        flist.append(XML.setFname()+"AttackData.txt")
        
    # check if files exist
    for f in flist:
        if not os.path.exists(f):
            print(f'{f} does not exist!')
            exit()

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp1_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # print(flist)

def PlotExp1(flist, rdpath):
    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Convert lists to data for plotting (mean and standard deviation)
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFClist]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Caplist]

    # Prepare data for plotting
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Set up the x-axis for the number of detractors (0% to 50%)
    detractors_percentage = np.arange(0, 60, 10)

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Define font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Plot for Total Food Collected
    axs[0].errorbar(detractors_percentage, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractors_percentage, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Percentage of Detractors', fontsize=xlabel_fontsize)
    axs[1].set_ylabel('Robots Captured', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

     # Modify x-ticks to include the percent symbol
    percent_labels = [f"{int(value)}%" for value in detractors_percentage]
    axs[1].set_xticks(detractors_percentage)
    axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment1B_lineplot.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment1B_raw_data.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (10%)',
            'Misleading Trail Attack (20%)',
            'Misleading Trail Attack (30%)',
            'Misleading Trail Attack (40%)',
            'Misleading Trail Attack (50%)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

def PlotExp1_percentages(flist, rdpath, total_robots, total_food):
    
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]  

    # Calculate the percentage of robots captured
    Cap_percent = []
    for detractor_percentage, captured_data in zip(detractor_percentages, Caplist):
        normal_agents = total_robots - int((detractor_percentage / 100) * total_robots)
        Cap_percent.append((captured_data / normal_agents) * 100)

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(detractor_percentages, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractor_percentages, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Percentage of Detractors (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment1_lineplot.png'))
    plt.clf()

######### EXPERIMENT 2 #########

def Experiment2(rc):

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    XML.setBotCount(32)
    robot_count = 32
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp2B_new_r24_{run_count}it/'

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

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]     # Rates of laying pheromone

    flist = []

    XML.setDetractorPercentage(25)
    for p in lambda_list:
        XML.RLP_F = p
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack: Iteration: {j+1}/{run_count}, Rate of laying pheromone: {p}%\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp2_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    PlotExp2_percentages_t2c(flist, XML.RD_PATH, resource_count)

def Experiment2_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 32
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(25) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp2B_new_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    rlp_list = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]     # Rates of laying pheromone

    flist = []

    # flist.append(XML.setFname()+"AttackData.txt")

    for p in rlp_list:

        XML.RLP_F = p
        flist.append(XML.setFname()+"AttackData.txt")
        
    # check if files exist
    for f in flist:
        if not os.path.exists(f):
            print(f'{f} does not exist!')
            exit()

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp2_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # PlotExp2_percentages_t2c(flist, XML.RD_PATH, resource_count)
    # print(flist)

    GetCorrelationMatrix(flist, XML.RD_PATH)

def PlotExp2(flist, rdpath):
    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Convert lists to data for plotting (mean and standard deviation)
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFClist]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Caplist]

    # Prepare data for plotting
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Set up the x-axis for the number of detractors (0% to 50%)
    detractors_percentage = np.arange(0, 60, 10)

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Define font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Plot for Total Food Collected
    axs[0].errorbar(detractors_percentage, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractors_percentage, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize)
    axs[1].set_ylabel('Robots Captured', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

     # Modify x-ticks to include the percent symbol
    percent_labels = [f"{int(value)}%" for value in detractors_percentage]
    axs[1].set_xticks(detractors_percentage)
    axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2_lineplot.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2_raw_data.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (10%)',
            'Misleading Trail Attack (20%)',
            'Misleading Trail Attack (30%)',
            'Misleading Trail Attack (40%)',
            'Misleading Trail Attack (50%)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

def PlotExp2_percentages(flist, rdpath, total_robots, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    # detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages
    rlp_list = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]  # List of pheromone rates

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]  

    # Calculate the percentage of robots captured
    # Cap_percent = [(data / (total_robots * 0.75)) * 100 for data in Caplist]  # 25% are detractors, so 75% are normal agents
    # Calculate the percentage of robots captured
    Cap_percent = [(data / total_robots) * 100 for data in Caplist]

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(rlp_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(rlp_list, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2B_lineplot_percentages.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2B_raw.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (RLP = 1.0)',
            'Misleading Trail Attack (RLP = 2.0)',
            'Misleading Trail Attack (RLP = 3.0)',
            'Misleading Trail Attack (RLP = 4.0)',
            'Misleading Trail Attack (RLP = 5.0)',
            'Misleading Trail Attack (RLP = 6.0)',
            'Misleading Trail Attack (RLP = 7.0)',
            'Misleading Trail Attack (RLP = 8.0)',
            'Misleading Trail Attack (RLP = 9.0)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

# t2c = time to capture all bots
def PlotExp2_percentages_t2c(flist, rdpath, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    SimTimeList = []  # Simulation Time List
    rlp_list = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]  # List of pheromone rates

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        SimTimeList.append(np.array(SIM_TIME).astype(float))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    # Calculate mean and standard deviation for the percentages of food collected
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]

    # Calculate mean and standard deviation for simulation time
    SimTimeData = [(round(np.mean(data), 1), np.std(data)) for data in SimTimeList]

    for d1 in SimTimeList:
        for d2 in d1:
            if (d2 > 1800):
                print('Simulation time is greater than 1800 seconds!')
                exit()

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    sim_time_mean = [x[0] for x in SimTimeData]
    sim_time_stdev = [x[1] for x in SimTimeData]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(rlp_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Time to Capture All Bots
    axs[1].errorbar(rlp_list, sim_time_mean, yerr=sim_time_stdev, fmt='o-', color='red', capsize=5, alpha = 0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Time to Capture All Bots (s)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2B_t2c_lineplot_percentages.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2B_t2c_raw.txt')
    with open(raw_data_filename, 'w') as file:
        
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (RLP = 1.0)',
            'Misleading Trail Attack (RLP = 2.0)',
            'Misleading Trail Attack (RLP = 3.0)',
            'Misleading Trail Attack (RLP = 4.0)',
            'Misleading Trail Attack (RLP = 5.0)',
            'Misleading Trail Attack (RLP = 6.0)',
            'Misleading Trail Attack (RLP = 7.0)',
            'Misleading Trail Attack (RLP = 8.0)',
            'Misleading Trail Attack (RLP = 9.0)'
        ]
        for tfc, cap in zip(TFClist, SimTimeList):
            file.write(f'****************************************************************************************************\n')
            file.write(f'{exp_list[count]}\n')
            file.write(f'Resources Collected Mean: {food_collection_percent_mean[count]}, Resources Collected Stdev: {food_collection_percent_stdev[count]}\n')
            file.write(f'Time to Capture All Bots Mean: {sim_time_mean[count]}, Time to Capture All Bots Stdev: {sim_time_stdev[count]}\n')
            file.write(f'Raw Data:\n')
            file.write('Total Food Collected, Sim Time\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

######### EXPERIMENT 3 #########

def Experiment3(rc):

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
    XML.RD_PATH=f'results/results_Exp3_r24_redo_{run_count}it/'

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

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]     # Rates of laying pheromone

    flist = []

    XML.setDetractorPercentage(25)

    for p in lambda_list:
        XML.RLP_F = p
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack: Iteration: {j+1}/{run_count}, Rate of laying pheromone: {p}%\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp3_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    PlotExp3_percentages_t2c(flist, XML.RD_PATH, resource_count)

def Experiment3_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(25) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp3_r24_redo_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]     # Rates of laying pheromone

    flist = []

    # flist.append(XML.setFname()+"AttackData.txt")

    for p in rlp_list:

        XML.RLP_F = p
        flist.append(XML.setFname()+"AttackData.txt")
        
    # check if files exist
    for f in flist:
        if not os.path.exists(f):
            print(f'{f} does not exist!')
            exit()

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp3_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # PlotExp3_percentages_t2c(flist, XML.RD_PATH, resource_count)
    # print(flist)

    GetCorrelationMatrix(flist, XML.RD_PATH)

def PlotExp3(flist, rdpath):
    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Convert lists to data for plotting (mean and standard deviation)
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFClist]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Caplist]

    # Prepare data for plotting
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Set up the x-axis for the number of detractors (0% to 50%)
    detractors_percentage = np.arange(0, 60, 10)

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Define font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Plot for Total Food Collected
    axs[0].errorbar(detractors_percentage, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractors_percentage, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize)
    axs[1].set_ylabel('Robots Captured', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

     # Modify x-ticks to include the percent symbol
    percent_labels = [f"{int(value)}%" for value in detractors_percentage]
    axs[1].set_xticks(detractors_percentage)
    axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2_lineplot.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2_raw_data.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (10%)',
            'Misleading Trail Attack (20%)',
            'Misleading Trail Attack (30%)',
            'Misleading Trail Attack (40%)',
            'Misleading Trail Attack (50%)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

def PlotExp3_percentages(flist, rdpath, total_robots, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    # detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages
    rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"] # List of pheromone rates

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    for tfc in TFC_percent:
        for t in tfc:
            
            if (t > 100):
                print('Food collected is greater than 100%!')
                exit()
            elif (t < 0):
                print('Food collected is less than 0%!')
                exit()

    # Calculate the percentage of robots captured
    Cap_percent = [(data / (total_robots * 0.75)) * 100 for data in Caplist]  # 25% are detractors, so 75% are normal agents

    for cap in Cap_percent:
        for c in cap:
            if (c > 100):
                print('Robots captured is greater than 100%!')
                exit()
            elif (c < 0):
                print('Robots captured is less than 0%!')
                exit()

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(rlp_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(rlp_list, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment3_lineplot_percentages.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment3_raw.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (RLP = 1.0)',
            'Misleading Trail Attack (RLP = 2.0)',
            'Misleading Trail Attack (RLP = 3.0)',
            'Misleading Trail Attack (RLP = 4.0)',
            'Misleading Trail Attack (RLP = 5.0)',
            'Misleading Trail Attack (RLP = 6.0)',
            'Misleading Trail Attack (RLP = 7.0)',
            'Misleading Trail Attack (RLP = 8.0)',
            'Misleading Trail Attack (RLP = 9.0)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

# t2c = time to capture all bots
def PlotExp3_percentages_t2c(flist, rdpath, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    SimTimeList = []  # Simulation Time List
    rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]  # List of pheromone rates

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        SimTimeList.append(np.array(SIM_TIME).astype(float))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    # Calculate mean and standard deviation for the percentages of food collected
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]

    # Calculate mean and standard deviation for simulation time
    SimTimeData = [(round(np.mean(data), 1), np.std(data)) for data in SimTimeList]

    for d1 in SimTimeList:
        for d2 in d1:
            if (d2 > 1800):
                print('Simulation time is greater than 1800 seconds!')
                exit()

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    sim_time_mean = [x[0] for x in SimTimeData]
    sim_time_stdev = [x[1] for x in SimTimeData]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(rlp_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Time to Capture All Bots
    axs[1].errorbar(rlp_list, sim_time_mean, yerr=sim_time_stdev, fmt='o-', color='red', capsize=5, alpha = 0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Time to Capture All Bots (s)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2B_t2c_lineplot_percentages.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2B_t2c_raw.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (RLP = 1.0)',
            'Misleading Trail Attack (RLP = 2.0)',
            'Misleading Trail Attack (RLP = 3.0)',
            'Misleading Trail Attack (RLP = 4.0)',
            'Misleading Trail Attack (RLP = 5.0)',
            'Misleading Trail Attack (RLP = 6.0)',
            'Misleading Trail Attack (RLP = 7.0)',
            'Misleading Trail Attack (RLP = 8.0)',
            'Misleading Trail Attack (RLP = 9.0)'
        ]
        for tfc, cap in zip(TFClist, SimTimeList):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1


######### EXPERIMENT 4 (DEFENSE) #########

def Experiment4(rc):

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
    XML.RD_PATH=f'results/results_Exp4_r{robot_count}_noCG_st{XML.MAX_SIM_TIME}_rc{run_count}it/'
    XML.UseMisleadingTrailAttack(True)

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

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    # lambda_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]     # Rates of laying pheromone
    tolerance_list = [0.1, 0.2, 0.3, 0.4, 0.5]      # time estimation tolerance

    flist = []

    XML.setDetractorPercentage(25)
    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.STRIKE_LIMIT = 5

    for t in tolerance_list:
        XML.TTT= t
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack: Iteration: {j+1}/{run_count}, Travel Time Tolerance: {t}\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp4_percentages(flist, XML.RD_PATH, robot_count, resource_count)



    flist = []

    XML.RD_PATH=f'results/results_Exp4_r{robot_count}_CG_st{XML.MAX_SIM_TIME}_rc{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    XML.USE_DEF_CG = "true"

    for t in tolerance_list:
        XML.TTT= t
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack: Iteration: {j+1}/{run_count}, Travel Time Tolerance: {t}%\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp4_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # PlotExp3_percentages_t2c(flist, XML.RD_PATH, resource_count)
    

def Experiment4_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(25) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp3_r24_redo_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]     # Rates of laying pheromone

    flist = []

    # flist.append(XML.setFname()+"AttackData.txt")

    for p in rlp_list:

        XML.RLP_F = p
        flist.append(XML.setFname()+"AttackData.txt")
        
    # check if files exist
    for f in flist:
        if not os.path.exists(f):
            print(f'{f} does not exist!')
            exit()

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp3_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # PlotExp3_percentages_t2c(flist, XML.RD_PATH, resource_count)
    # print(flist)

    GetCorrelationMatrix(flist, XML.RD_PATH)

def PlotExp4(flist, rdpath):
    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Convert lists to data for plotting (mean and standard deviation)
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFClist]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Caplist]

    # Prepare data for plotting
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Set up the x-axis for the number of detractors (0% to 50%)
    detractors_percentage = np.arange(0, 60, 10)

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Define font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Plot for Total Food Collected
    axs[0].errorbar(detractors_percentage, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractors_percentage, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize)
    axs[1].set_ylabel('Robots Captured', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

     # Modify x-ticks to include the percent symbol
    percent_labels = [f"{int(value)}%" for value in detractors_percentage]
    axs[1].set_xticks(detractors_percentage)
    axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2_lineplot.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2_raw_data.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (10%)',
            'Misleading Trail Attack (20%)',
            'Misleading Trail Attack (30%)',
            'Misleading Trail Attack (40%)',
            'Misleading Trail Attack (50%)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

def PlotExp4_percentages(flist, rdpath, total_robots, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    # detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages
    # rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"] # List of pheromone rates
    ttt_list = [10, 20, 30, 40, 50] # List of travel time tolerance

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    for tfc in TFC_percent:
        for t in tfc:
            
            if (t > 100):
                print('Food collected is greater than 100%!')
                exit()
            elif (t < 0):
                print('Food collected is less than 0%!')
                exit()

    # Calculate the percentage of robots captured
    Cap_percent = [(data / (total_robots * 0.75)) * 100 for data in Caplist]  # 25% are detractors, so 75% are normal agents

    for cap in Cap_percent:
        for c in cap:
            if (c > 100):
                print('Robots captured is greater than 100%!')
                exit()
            elif (c < 0):
                print('Robots captured is less than 0%!')
                exit()

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(ttt_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(ttt_list, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Travel Time Tolerance (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment3_lineplot_percentages.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment3_raw.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (RLP = 1.0)',
            'Misleading Trail Attack (RLP = 2.0)',
            'Misleading Trail Attack (RLP = 3.0)',
            'Misleading Trail Attack (RLP = 4.0)',
            'Misleading Trail Attack (RLP = 5.0)',
            'Misleading Trail Attack (RLP = 6.0)',
            'Misleading Trail Attack (RLP = 7.0)',
            'Misleading Trail Attack (RLP = 8.0)',
            'Misleading Trail Attack (RLP = 9.0)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

# t2c = time to capture all bots
def PlotExp4_percentages_t2c(flist, rdpath, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    SimTimeList = []  # Simulation Time List
    # rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]  # List of pheromone rates
    ttt_list = [0.1, 0.2, 0.3, 0.4, 0.5] # List of travel time tolerance

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        SimTimeList.append(np.array(SIM_TIME).astype(float))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    # Calculate mean and standard deviation for the percentages of food collected
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]

    # Calculate mean and standard deviation for simulation time
    SimTimeData = [(round(np.mean(data), 1), np.std(data)) for data in SimTimeList]

    for d1 in SimTimeList:
        for d2 in d1:
            if (d2 > 1800):
                print('Simulation time is greater than 1800 seconds!')
                exit()

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    sim_time_mean = [x[0] for x in SimTimeData]
    sim_time_stdev = [x[1] for x in SimTimeData]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(ttt_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Time to Capture All Bots
    axs[1].errorbar(ttt_list, sim_time_mean, yerr=sim_time_stdev, fmt='o-', color='red', capsize=5, alpha = 0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Time to Capture All Bots (s)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment2B_t2c_lineplot_percentages.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment2B_t2c_raw.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (RLP = 1.0)',
            'Misleading Trail Attack (RLP = 2.0)',
            'Misleading Trail Attack (RLP = 3.0)',
            'Misleading Trail Attack (RLP = 4.0)',
            'Misleading Trail Attack (RLP = 5.0)',
            'Misleading Trail Attack (RLP = 6.0)',
            'Misleading Trail Attack (RLP = 7.0)',
            'Misleading Trail Attack (RLP = 8.0)',
            'Misleading Trail Attack (RLP = 9.0)'
        ]
        for tfc, cap in zip(TFClist, SimTimeList):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1



######### EXPERIMENT 5 and 6 (DEFENSE) #########

def Experiment5_6(rc):

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
    # XML.RD_PATH=f'results/results_Exp5_r{robot_count}_noCG_st{XML.MAX_SIM_TIME}_rc{run_count}it/'
    XML.UseMisleadingTrailAttack(True)

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

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    ######### Experiment 5 ########

    lambda_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]     # Rates of laying pheromone

    flist = []

    XML.RD_PATH=f'results/results_Exp5_r{robot_count}_layrate_st{XML.MAX_SIM_TIME}_rc{run_count}it/'

    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    XML.USE_DEF_CG = "true"

    for p in lambda_list:
        XML.RLP_F= p
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack: Iteration: {j+1}/{run_count}, Lay Rate: {p}%\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp5_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    
    ####### Experiment 6 ########

    det_percent_list = [0, 10, 20, 30, 40, 50]  # List of detractor percentages

    flist = []

    XML.RD_PATH=f'results/results_Exp6_r{robot_count}_detpercent_st{XML.MAX_SIM_TIME}_rc{run_count}it/'


    if (not DirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not DirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    XML.RLP_F = "4.0"     # from experiment 3, 4.0 has most robots captured

    for d in det_percent_list:
        XML.setDetractorPercentage(d)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Attack: Iteration: {j+1}/{run_count}, Detractor Percentage: {d}%\n')
            os.system("argos3 -c ./experiments/Misleading_Trail_1.xml")

    PlotExp6_percentages(flist, XML.RD_PATH, robot_count, resource_count)

def Experiment5_replot(rc):

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
    XML.RD_PATH=f'results/results_Exp5_r{robot_count}_noCG_st{XML.MAX_SIM_TIME}_rc{run_count}it/'
    XML.UseMisleadingTrailAttack(True)

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    lambda_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]     # Rates of laying pheromone
    # tolerance_list = [0.1, 0.2, 0.3, 0.4, 0.5]      # time estimation tolerance

    flist = []

    XML.setDetractorPercentage(25)
    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.STRIKE_LIMIT = 5

    for p in lambda_list:
        XML.RLP_F= p
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        
    PlotExp5B_percentages(flist, XML.RD_PATH, robot_count, resource_count)



    flist = []

    XML.RD_PATH=f'results/results_Exp5_r{robot_count}_CG_st{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.USE_DEF_CG = "true"

    for p in lambda_list:
        XML.RLP_F= p
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()

    PlotExp5B_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # PlotExp3_percentages_t2c(flist, XML.RD_PATH, resource_count)

def PlotExp5_percentages(flist, rdpath, total_robots, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    # detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages
    rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"] # List of pheromone rates
    # ttt_list = [10, 20, 30, 40, 50] # List of travel time tolerance

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    for tfc in TFC_percent:
        for t in tfc:
            
            if (t > 100):
                print('Food collected is greater than 100%!')
                exit()
            elif (t < 0):
                print('Food collected is less than 0%!')
                exit()

    # Calculate the percentage of robots captured
    Cap_percent = [(data / (total_robots * 0.75)) * 100 for data in Caplist]  # 25% are detractors, so 75% are normal agents

    for cap in Cap_percent:
        for c in cap:
            if (c > 100):
                print('Robots captured is greater than 100%!')
                exit()
            elif (c < 0):
                print('Robots captured is less than 0%!')
                exit()

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(rlp_list, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(rlp_list, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Travel Time Tolerance (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment5_lineplot_percentages.png'))
    plt.clf()

def PlotExp5B_percentages(flist, rdpath, total_robots, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    Isolist = []  # Total Food Collected List
    FPlist = []  # Robots Captured List
    # detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages
    rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"] # List of pheromone rates
    # ttt_list = [10, 20, 30, 40, 50] # List of travel time tolerance

    for filename in flist:
        Read(filename)
        Isolist.append(np.array(TOTAL_ISOLATED_BOTS).astype(int))
        FPlist.append(np.array(NUM_FALSE_POSITIVES).astype(int))

    # Calculate the percentage of food collected
    # TFC_percent = [(data / total_food) * 100 for data in TFClist]

    # Calculate the percentage of isolated robots
    Iso_percent = [(data / total_robots) * 100 for data in Isolist]

    # for tfc in TFC_percent:
    #     for t in tfc:
            
    #         if (t > 100):
    #             print('Food collected is greater than 100%!')
    #             exit()
    #         elif (t < 0):
    #             print('Food collected is less than 0%!')
    #             exit()

    # Calculate the percentage of robots captured
    # Cap_percent = [(data / (total_robots * 0.75)) * 100 for data in Caplist]  # 25% are detractors, so 75% are normal agents

    # for cap in Cap_percent:
    #     for c in cap:
    #         if (c > 100):
    #             print('Robots captured is greater than 100%!')
    #             exit()
    #         elif (c < 0):
    #             print('Robots captured is less than 0%!')
    #             exit()

    # Calculate mean and standard deviation for the percentages
    Isodata = [(round(np.mean(data), 1), np.std(data)) for data in Iso_percent]
    FPdata = [(round(np.mean(data), 1), np.std(data)) for data in FPlist]

    # Prepare data for plotting
    # food_collection_percent_mean = [x[0] for x in TFCdata]
    isolated_robots_percent_mean = [x[0] for x in Isodata]
    # food_collection_percent_stdev = [x[1] for x in TFCdata]
    isolated_robots_percent_stdev = [x[1] for x in Isodata]
    # robot_captured_percent_mean = [x[0] for x in Capdata]
    false_positive_mean = [x[0] for x in FPdata]
    # robot_captured_percent_stdev = [x[1] for x in Capdata]
    false_positive_stdev = [x[1] for x in FPdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(rlp_list, isolated_robots_percent_mean, yerr=isolated_robots_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Isolated Robots (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(rlp_list, false_positive_mean, yerr=false_positive_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Rate of Laying Pheromone (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('False Positives', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment5B_lineplot_percentages.png'))
    plt.clf()

def PlotExp6_percentages(flist, rdpath, total_robots, total_food):
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages
    # rlp_list = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"] # List of pheromone rates
    # ttt_list = [10, 20, 30, 40, 50] # List of travel time tolerance

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]

    for tfc in TFC_percent:
        for t in tfc:
            
            if (t > 100):
                print('Food collected is greater than 100%!')
                exit()
            elif (t < 0):
                print('Food collected is less than 0%!')
                exit()

    # Calculate the percentage of robots captured
    Cap_percent = []
    for detractor_percentage, captured_data in zip(detractor_percentages, Caplist):
        normal_agents = total_robots - int((detractor_percentage / 100) * total_robots)
        Cap_percent.append((captured_data / normal_agents) * 100)

    for cap in Cap_percent:
        for c in cap:
            if (c > 100):
                print('Robots captured is greater than 100%!')
                exit()
            elif (c < 0):
                print('Robots captured is less than 0%!')
                exit()

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(detractor_percentages, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractor_percentages, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Detractor Percentage (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment6_lineplot_percentages.png'))
    plt.clf()

######### EXPERIMENT 6 static number of foragers, varying detractors #########

def Experiment6(rc):

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    sim_time = 2700
    XML.MAX_SIM_TIME = sim_time     # increased from 1800 to 2700 (+50%)
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp6_noDef_r24_st{sim_time}_{run_count}it/'

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

    percent_list = [0, 10, 20, 30, 40, 50]     # Percentage of detractors

    XML.RLP_F = "4.0"     # Experiment 3: rate = 4.0 has most robots captured

    flist = []

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    for p in percent_list:
        XML.setDetractorPercentage(p, True)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp6_percentages(flist, XML.RD_PATH, total_robots, total_food, True)

    flist = []

    XML.RD_PATH=f'results/results_Exp6_r24_st{sim_time}_{run_count}it/'

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

    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.USE_DEF_CG = "true"

    for p in percent_list:
        XML.setDetractorPercentage(p, True)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp6_percentages(flist, XML.RD_PATH, total_robots, total_food, False)

def Experiment6_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 2700
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(0) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_noDef_r24_st2700_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    percent_list = [10, 20, 30, 40, 50]
    XML.RLP_F = "4.0"
    flist = []

    flist.append(XML.setFname()+"AttackData.txt")

    for p in percent_list:

        XML.setDetractorPercentage(p)
        flist.append(XML.setFname()+"AttackData.txt")
        
    # check if files exist
    for f in flist:
        if not os.path.exists(f):
            print(f'{f} does not exist!')
            exit()

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp1_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # print(flist)

def PlotExp6(flist, rdpath):
    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Convert lists to data for plotting (mean and standard deviation)
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFClist]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Caplist]

    # Prepare data for plotting
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Set up the x-axis for the number of detractors (0% to 50%)
    detractors_percentage = np.arange(0, 60, 10)

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Define font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Plot for Total Food Collected
    axs[0].errorbar(detractors_percentage, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractors_percentage, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Percentage of Detractors', fontsize=xlabel_fontsize)
    axs[1].set_ylabel('Robots Captured', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

     # Modify x-ticks to include the percent symbol
    percent_labels = [f"{int(value)}%" for value in detractors_percentage]
    axs[1].set_xticks(detractors_percentage)
    axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment1B_lineplot.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment1B_raw_data.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (10%)',
            'Misleading Trail Attack (20%)',
            'Misleading Trail Attack (30%)',
            'Misleading Trail Attack (40%)',
            'Misleading Trail Attack (50%)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

def PlotExp6_percentages(flist, rdpath, total_robots, total_food, noDef):
    
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]  

    # Calculate the percentage of robots captured
    Cap_percent = []
    for detractor_percentage, captured_data in zip(detractor_percentages, Caplist):
        normal_agents = total_robots - int((detractor_percentage / 100) * total_robots)
        Cap_percent.append((captured_data / normal_agents) * 100)

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(detractor_percentages, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractor_percentages, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Percentage of Detractors (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    if (noDef):
        plt.savefig(os.path.join(rdpath, 'Experiment6_noDef_lineplot.png'))
    else:
        plt.savefig(os.path.join(rdpath, 'Experiment6_lineplot.png'))
    plt.clf()

######### EXPERIMENT 7 #########
    
# This experiment explores increasing misleading trails by forcing the detractors to always lay 4 pheromone trails (one to each attack nest) each time they lay a trail.

def Experiment7(rc):

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    sim_time = 1800
    XML.MAX_SIM_TIME = sim_time     # increased from 1800 to 2700 (+50%)
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.BOT_COUNT = total_robots
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_IncreaseTrails_r24_rlp4_st{sim_time}_{run_count}it/'
    XML.INC_MLT = "true"

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

    percent_list = [0, 10, 20, 30, 40, 50]     # Percentage of detractors

    XML.RLP_F = "4.0"     # Experiment 3: rate = 8.0 has least performance

    flist = []

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

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    for p in percent_list:
        XML.setDetractorPercentage(p, True)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp6_percentages(flist, XML.RD_PATH, total_robots, total_food, False)

def Experiment7_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 2700
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 24
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(0) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_noDef_r24_st2700_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    percent_list = [10, 20, 30, 40, 50]
    XML.RLP_F = "4.0"
    flist = []

    flist.append(XML.setFname()+"AttackData.txt")

    for p in percent_list:

        XML.setDetractorPercentage(p)
        flist.append(XML.setFname()+"AttackData.txt")
        
    # check if files exist
    for f in flist:
        if not os.path.exists(f):
            print(f'{f} does not exist!')
            exit()

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp1_percentages(flist, XML.RD_PATH, robot_count, resource_count)
    # print(flist)

def PlotExp7(flist, rdpath):
    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Convert lists to data for plotting (mean and standard deviation)
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFClist]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Caplist]

    # Prepare data for plotting
    food_collection_mean = [x[0] for x in TFCdata]
    food_collection_stdev = [x[1] for x in TFCdata]
    robot_captured_mean = [x[0] for x in Capdata]
    robot_captured_stdev = [x[1] for x in Capdata]

    # Set up the x-axis for the number of detractors (0% to 50%)
    detractors_percentage = np.arange(0, 60, 10)

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Define font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Plot for Total Food Collected
    axs[0].errorbar(detractors_percentage, food_collection_mean, yerr=food_collection_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractors_percentage, robot_captured_mean, yerr=robot_captured_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Percentage of Detractors', fontsize=xlabel_fontsize)
    axs[1].set_ylabel('Robots Captured', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

     # Modify x-ticks to include the percent symbol
    percent_labels = [f"{int(value)}%" for value in detractors_percentage]
    axs[1].set_xticks(detractors_percentage)
    axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment1B_lineplot.png'))
    plt.clf()

    # Write the raw data to a text file
    raw_data_filename = os.path.join(rdpath, 'Experiment1B_raw_data.txt')
    with open(raw_data_filename, 'w') as file:
        file.write('Total Food Collected, Robots Captured\n')
        count = 0
        exp_list = [
            'Standard CPFA',
            'Misleading Trail Attack (10%)',
            'Misleading Trail Attack (20%)',
            'Misleading Trail Attack (30%)',
            'Misleading Trail Attack (40%)',
            'Misleading Trail Attack (50%)'
        ]
        for tfc, cap in zip(TFClist, Caplist):
            file.write(f'{exp_list[count]}\n')
            for f, c in zip(tfc, cap):
                file.write(f'{f}, {c}\n')
            count += 1

def PlotExp7_percentages(flist, rdpath, total_robots, total_food, noDef):
    
    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    TFClist = []  # Total Food Collected List
    Caplist = []  # Robots Captured List
    detractor_percentages = [0, 10, 20, 30, 40, 50]  # List of detractor percentages

    for filename in flist:
        Read(filename)
        TFClist.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate the percentage of food collected
    TFC_percent = [(data / total_food) * 100 for data in TFClist]  

    # Calculate the percentage of robots captured
    Cap_percent = []
    for detractor_percentage, captured_data in zip(detractor_percentages, Caplist):
        normal_agents = total_robots - int((detractor_percentage / 100) * total_robots)
        Cap_percent.append((captured_data / normal_agents) * 100)

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Prepare data for plotting
    food_collection_percent_mean = [x[0] for x in TFCdata]
    food_collection_percent_stdev = [x[1] for x in TFCdata]
    robot_captured_percent_mean = [x[0] for x in Capdata]
    robot_captured_percent_stdev = [x[1] for x in Capdata]

    # Start plotting
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    axs[0].errorbar(detractor_percentages, food_collection_percent_mean, yerr=food_collection_percent_stdev, fmt='o-', label='Food Collection', color='blue', capsize=5, alpha=0.7, linewidth=2)
    axs[0].set_ylabel('Resources Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axs[0].grid(True)
    axs[0].tick_params(axis='y', labelsize=y_tick_fontsize)

    # Plot for Robots Captured
    axs[1].errorbar(detractor_percentages, robot_captured_percent_mean, yerr=robot_captured_percent_stdev, fmt='o-', label='Robots Captured', color='red', capsize=5, alpha=0.7, linewidth=2)
    axs[1].set_xlabel('Percentage of Detractors (%)', fontsize=xlabel_fontsize, labelpad=15)
    axs[1].set_ylabel('Robots Captured (%)', fontsize=ylabel_fontsize)
    axs[1].grid(True)
    axs[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=y_tick_fontsize)

    # # Modify x-ticks to include the percent symbol
    # percent_labels = [f"{value}%" for value in detractor_percentages]
    # axs[1].set_xticks(detractor_percentages)
    # axs[1].set_xticklabels(percent_labels)

    plt.tight_layout()
    if (noDef):
        plt.savefig(os.path.join(rdpath, 'Experiment6_noDef_lineplot.png'))
    else:
        plt.savefig(os.path.join(rdpath, 'Experiment6_lineplot.png'))
    plt.clf()

######### EXPERIMENT 8 #########
    
# This experiment explores increasing misleading trails by increasing the rate of laying pheromnes for detractors and possibly decreasing that of foragers

def Experiment8(rc):

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    sim_time = 1800
    XML.MAX_SIM_TIME = sim_time     # increased from 1800 to 2700 (+50%)
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.BOT_COUNT = total_robots
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_RateIncrease_r24_rlpf6_rlpd1_st{sim_time}_{run_count}it/'
    # XML.INC_MLT = "true"
    XML.LET_DET_USE_MLT = "false"

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

    percent_list = [0, 10, 20, 30, 40, 50]     # Percentage of detractors

    # Set detractors to have a higher rate of laying pheromones
    XML.RLP_F = "6.0"
    XML.RLP_D = "1.0"

    flist = []

    XML.USE_DEF = "false"
    XML.USE_DEF_CL = "false"
    XML.USE_DEF_CG = "false"

    for p in percent_list:
        XML.setDetractorPercentage(p, True)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp6_percentages(flist, XML.RD_PATH, total_robots, total_food, False)

######### EXPERIMENT 9 (w/ def) #########
    
# This experiment explores increasing misleading trails by increasing the rate of laying pheromnes for detractors and possibly decreasing that of foragers
# We are also implementing the defense now

def Experiment9(rc):

    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    sim_time = 1800
    XML.MAX_SIM_TIME = sim_time
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    total_robots = 24
    XML.BOT_COUNT = total_robots
    XML.setBotCount(total_robots)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_RateIncrease_DEF_r24_rlpf4_rlpd1_st{sim_time}_{run_count}it/'
    # XML.INC_MLT = "true"
    XML.LET_DET_USE_MLT = "false"

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

    percent_list = [0, 10, 20, 30, 40, 50]     # Percentage of detractors

    # Set detractors to have a higher rate of laying pheromones
    XML.RLP_F = "4.0"
    XML.RLP_D = "1.0"

    flist = []

    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.USE_DEF_CG = "true"

    for p in percent_list:
        XML.setDetractorPercentage(p, True)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    # PlotExp6_percentages(flist, XML.RD_PATH, total_robots, total_food, False)



if __name__ == "__main__":

    # Experiment1(30)
    # Experiment1_replot(30)

    # Experiment2(30)
    # Experiment2_replot(30)

    # Experiment3(30)
    # Experiment3_replot(30)

    # Experiment4(30)

    # Experiment5(30)
    # Experiment5_replot(30)

    # Experiment6(30)

    # Experiment7(30)

    # Experiment8(30)

    Experiment9(30)

    # quickTest()




















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
