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


def Read2(fname):
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
    XML.VISUAL = False
    XML.Densify(False)
    XML.UseQZone(False)
    XML.UseFFDoS(False)
    XML.UseMisleadingTrailAttack(True)
    XML.setBotCount(24)
    XML.MAX_SIM_TIME = 1500
    XML.setDistribution(1)
    XML.DRAW_TRAILS = 1
    # XML.NUM_DETRACTORS = 4
    XML.NUM_ATK_NESTS = 4

    XML.setDetractorPercentage(25)
    XML.RANDOM_SEED = 392160
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

    for i in range(run_count):
        XML.RLP = "4.0"
        # XML.FLW = 0.5
        XML.USE_DEF = "true"
        XML.USE_DEF_CL = "true"
        XML.USE_DEF_CG = "true"
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
            XML.RLP = p
            XML.createXML()
            print(f'Lambda: {XML.RLP}\n')
            
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
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    XML.setBotCount(24)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1_noDef_r24_{run_count}it/'

    XML.XML_FNAME = "./experiments/Misleading_Trail_2_exp1_noatk.xml"

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

    percent_list = [0, 10, 20, 30, 40, 50]     # Percentage of detractors

    XML.RLP = "4.0"     # Experiment 3: rate = 4.0 has most robots captured

    flist = []

    XML.USE_DEF = "false"

    for p in percent_list:
        XML.setDetractorPercentage(p)
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        for j in range(run_count):
            time.sleep(0.05)
            print(f'Iteration: {j+1}/{run_count}, Percentage Detractors: {p}%\n')
            os.system(f'argos3 -c {XML.XML_FNAME}')

    # PlotExp1(flist, XML.RD_PATH)
    PlotExp1_percentages(flist, XML.RD_PATH)

def Experiment1_replot(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1800
    XML.Densify(False)  # Don't use increased density for fake food (no fake food here. set just incase)
    robot_count = 32
    XML.setBotCount(robot_count)
    XML.setDetractorPercentage(0) # 0% detractors (to get baseline CPFA data)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    XML.RD_PATH=f'results/results_Exp1B_{run_count}it/'

    # Cluster Distribution Settings
    XML.NUM_RCL = 8
    XML.RCL_X = 6
    XML.RCL_Y = 6

    resource_count = XML.NUM_RCL * XML.RCL_X * XML.RCL_Y

    percent_list = [10, 20, 30, 40, 50]

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
        XML.RLP = p
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

        XML.RLP = p
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
        XML.RLP = p
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

        XML.RLP = p
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

        XML.RLP = p
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

    XML.USE_DEF = "true"
    XML.USE_DEF_CL = "true"
    XML.USE_DEF_CG = "true"
    XML.setDetractorPercentage(25)

    for p in lambda_list:
        XML.RLP= p
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

    XML.RLP = "4.0"     # from experiment 3, 4.0 has most robots captured

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
        XML.RLP= p
        flist.append(XML.setFname()+"AttackData.txt")
        XML.createXML()
        
    PlotExp5B_percentages(flist, XML.RD_PATH, robot_count, resource_count)



    flist = []

    XML.RD_PATH=f'results/results_Exp5_r{robot_count}_CG_st{XML.MAX_SIM_TIME}_rc{run_count}it/'

    XML.USE_DEF_CG = "true"

    for p in lambda_list:
        XML.RLP= p
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


####### Plot Tests ########

def PlotExp3_v3(flist, rdpath, maxRealFood, maxFakeFood, x_ticks):

    RFClist = []
    FFClist = []
    FPlist = []

    for filename in flist:
        Read(filename)
        RFClist.append(np.array(REAL_FOOD_COLLECTED).astype(float))
        FFClist.append(np.array(FAKE_FOOD_COLLECTED).astype(float))
        # FFClist.append(np.random.randint(0,108,(1,60)).astype(float))
        FPlist.append(np.array(FALSE_POSITIVES).astype(float))
        # FPlist.append(np.random.randint(0,90,(1,60)).astype(float))

    RFCdata = []
    for r in RFClist:
        RFCdata.append((round(np.mean(r),1),np.std(r)))
    print (len(RFCdata))
    FFCdata = []
    for f in FFClist:
        FFCdata.append((round(np.mean(f),1),np.std(f)))
    print (len(FFCdata))
    FPdata = []
    for p in FPlist:
        FPdata.append((round(np.mean(p),1),np.std(p)))
    print (len(FPdata))
    x_tick_labels = []
    for x in x_ticks:
        # if x*100 % 2:
        x_tick_labels.append(f'{int(x*100)}%')

    data1 = [
        ('$FA_{R}$',                (RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0]),
                                    (RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1]),
                                    (FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0],FPdata[0][0]),
                                    (FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1],FPdata[0][1]),
                                    (FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0]),
                                    (FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1])),
        
        ('$FA_{FR}$',               (RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0],RFCdata[1][0]),
                                    (RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1],RFCdata[1][1]),
                                    (FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0],FPdata[1][0]),
                                    (FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1],FPdata[1][1]),
                                    (FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0],FFCdata[1][0]),
                                    (FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1],FFCdata[1][1]))
    ]

    # RFCdata = [std, ff, qz100, qzm100, qz95, qzm95, qz90, qzm90]

    # data1 = [rfc]

    sim_type = ['$FA_{QZ}$','$FA_{QZ\_M}$']
    for i in range(len(sim_type)):
        rfc_m = []
        rfc_s = []
        fp_m = []
        fp_s = []
        ffc_m = []
        ffc_s = []
        for j in range(2+i,len(RFCdata),2):
            fp_m.append(FPdata[j][0])
            fp_s.append(FPdata[j][1])
            rfc_m.append(RFCdata[j][0])
            rfc_s.append(RFCdata[j][1])
            ffc_m.append(FFCdata[j][0])
            ffc_s.append(FFCdata[j][1])
        data1.append((sim_type[i], tuple(rfc_m), tuple(rfc_s), tuple(fp_m), tuple(fp_s), tuple(ffc_m), tuple(ffc_s)))

    x = np.arange(len(x_tick_labels))
    width=0.4
    multiplier=0

    fig,ax=plt.subplots(figsize=(14,10),nrows=3, sharex=True)
    labelsize = 14
    textsize = 23
    ticksize = 18
    top_plt_pad = -125
    bottom_plt_pad = 25
    top_labelcolor = 'white'
    bottom_labelcolor = 'black'
    bar_zorder = 0
    label_zorder = 15
    b_label_rotation = 30

    # offset = width * multiplier
    # rect1 = ax[0].bar(x+offset, data1[0][1], width, align="center", yerr=data1[0][2], ecolor='orange', label=data1[0][0], edgecolor='black', color='blue', zorder=bar_zorder)
    # ax[0].bar_label(rect1,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # multiplier+=1

    # offset = width * multiplier
    # rect3 = ax[0].bar(x+offset, data1[1][1], width, align="center", yerr=data1[1][2], ecolor='orange', label=data1[1][0], edgecolor='black', color='green', zorder=bar_zorder)
    # rect4 = ax[1].bar(x+offset, data1[1][3], width, align="center", yerr=data1[1][4], ecolor='orange', label=data1[1][0], edgecolor='black', hatch='xx', color='green', zorder=bar_zorder)
    # ax[0].bar_label(rect3,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # ax[1].bar_label(rect4,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # multiplier+=1

    offset = width * multiplier
    rect5 = ax[0].bar(x+offset, data1[2][1], width, align="center", yerr=data1[2][2], ecolor='orange', label=data1[2][0], edgecolor='black', color='red', zorder=bar_zorder)
    line1 = ax[0].axhline(data1[0][1][0], linestyle='dashed', color='blue', linewidth=2)
    rect6 = ax[1].bar(x+offset, data1[2][3], width, align="center", yerr=data1[2][4], ecolor='orange', label=data1[2][0], edgecolor='black', hatch='..', color='red', zorder=bar_zorder)
    rect7 = ax[2].bar(x+offset, data1[2][5], width, align="center", yerr=data1[2][6], ecolor='orange', label=data1[2][0], edgecolor='black', hatch='xx', color='red', zorder=bar_zorder)
    line2 = ax[2].axhline(data1[0][1][0], linestyle='dashed', color='blue', linewidth=2)
    # ax[0].bar_label(rect5,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # ax[1].bar_label(rect6,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # ax[2].bar_label(rect7,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect8 = ax[0].bar(x+offset, data1[3][1], width, align="center", yerr=data1[3][2], ecolor='orange', label=data1[3][0], edgecolor='black', color='purple', zorder=bar_zorder)
    line3 = ax[0].axhline(data1[1][1][0], linestyle='dashed', color='green', linewidth=2)
    rect9 = ax[1].bar(x+offset, data1[3][3], width, align="center", yerr=data1[3][4], ecolor='orange', label=data1[3][0], edgecolor='black', hatch='..', color='purple', zorder=bar_zorder)
    rect10 = ax[2].bar(x+offset, data1[3][5], width, align="center", yerr=data1[3][6], ecolor='orange', label=data1[3][0], edgecolor='black', hatch='xx', color='purple', zorder=bar_zorder)
    line4 = ax[2].axhline(data1[1][1][0], linestyle='dashed', color='green', linewidth=2)
    # ax[0].bar_label(rect8,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # ax[1].bar_label(rect9,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    # ax[2].bar_label(rect10,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1
    
    # ax[0].legend(loc='lower left', ncols=2, fontsize=textsize, bbox_to_anchor=(0, -0.1), zorder = 20)

    # First get the handles and labels from the axes
    # handles1, labels1 = ax[0].get_legend_handles_labels()
    # handles2, labels2 = ax[1].get_legend_handles_labels()
    # handles3, labels3 = ax[2].get_legend_handles_labels()
    # plt.legend(handles1, labels1, loc='lower left', ncol=2, fontsize=textsize)

    # ax[0].set_ylim(0,maxRealFood)
    ax[0].set_ylabel('Real Resources\n Collected', fontsize=textsize, labelpad=20)
    ax[1].set_ylabel('False Positives', fontsize=textsize, labelpad=20)
    ax[2].set_ylabel('Fake Resources\n Collected', fontsize=textsize, labelpad=20)

    ax[1].set_ylim(0,90)

    ax[0].tick_params(axis='both',labelsize=ticksize)
    ax[1].tick_params(axis='both',labelsize=ticksize)
    ax[2].tick_params(axis='both',labelsize=ticksize)
    ax[2].tick_params(axis='x', rotation=b_label_rotation)

    ax[2].set_xticks(x+width/2, x_tick_labels, fontsize=ticksize)
    ax[2].xaxis.tick_bottom()
    ax[2].set_xlabel('Fake Food Detection Accuracy', fontsize=textsize)


    fig.tight_layout()
    fig.subplots_adjust(hspace=0.1)

    plt.savefig(f'{rdpath}Experiment_3.png')

def plot_new_experiment(data, x_ticks, rdpath):
    """
    data: List containing tuples for each experiment condition. Each tuple should have the format:
          (label, real_food_collected, fake_food_collected, false_positives)
          where each element in real_food_collected, fake_food_collected, false_positives
          is a list of values for that condition.

    x_ticks: Labels for the x-axis.

    rdpath: Path to save the plot.
    """

    # Number of conditions (e.g., attack alone, attack with defense)
    num_conditions = len(data)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(14, 10))

    # Define positions for boxplots
    positions = np.arange(len(x_ticks)) * num_conditions * 1.5

    # Plotting each condition
    for i, (label, real_food, fake_food, false_positives) in enumerate(data):
        # Calculate positions for this condition's boxplots
        current_positions = positions + i * 0.5

        # Boxplot for real food collected
        ax.boxplot(real_food, positions=current_positions, widths=0.4, patch_artist=True, boxprops=dict(facecolor='C0'))

        # Add trend lines here (example: mean values)
        # Replace `np.mean(real_food, axis=1)` with your method of calculating the trend
        mean_values = np.mean(real_food, axis=1)
        ax.plot(current_positions, mean_values, label=label, marker='o', linestyle='-', linewidth=2)

        # Similar boxplots and trend lines for fake_food and false_positives can be added here

    # Setting the x-ticks and labels
    ax.set_xticks(np.arange(len(x_ticks)) * num_conditions)
    ax.set_xticklabels(x_ticks)

    # Adding labels and title
    ax.set_xlabel('Experiment Conditions', fontsize=12)
    ax.set_ylabel('Collected Resources', fontsize=12)
    ax.set_title('Comparison of Attack Alone vs Attack with Defense', fontsize=15)

    # Adding a legend
    ax.legend(loc='upper right')

    # Tight layout for better spacing
    plt.tight_layout()

    # Save the figure
    plt.savefig(f'{rdpath}New_Experiment_Plot.png')

    # Show the plot
    plt.show()

import re

def PlotExp_AtkDef_varyLayRate():

    # params
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24
    
    # get all filenames in directory for attack only
    flist_atk = []
    for filename in os.listdir("./results/results_Exp3_r24_30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_atk.append(os.path.join("./results/results_Exp3_r24_30it", filename))
        else:
            continue

    # get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/results_Exp5_r24_layrate_st1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/results_Exp5_r24_layrate_st1800_rc30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_atk.sort(key=extract_rlp_value)
    flist_atkdef.sort(key=extract_rlp_value)

    # print(flist_atk)
    # print(flist_atkdef)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_atk:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))
    
    TFClist_atkdef = []
    Caplist_atkdef = []
    for filename in flist_atkdef:
        Read(filename)
        TFClist_atkdef.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atkdef.append(np.array(ROBOTS_CAPTURED).astype(int))
    
    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / (total_robots * 0.75)) * 100 for data in Caplist_atk] # 25% are detractors, so 75% are normal agents
    TFC_percent_atkdef = [(data / total_food) * 100 for data in TFClist_atkdef]
    Cap_percent_atkdef = [(data / (total_robots * 0.75)) * 100 for data in Caplist_atkdef] # 25% are detractors, so 75% are normal agents

    # lay rates
    lay_rates = ["1.0", "4.0", "8.0", "12.0", "16.0", "20.0"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

    # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    positions_atk = np.arange(1, 2*num_rates, step=2)
    positions_atkdef = positions_atk + width + gap

    # Calculate positions for trend lines
    trend_positions_atk = positions_atk + width / 2
    trend_positions_atkdef = positions_atkdef + width / 2

    # Plot boxplots and trend lines
    for i in range(num_rates):
        # Boxplots
        axes[0].boxplot(TFC_percent_atk[i], positions=[positions_atk[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[0].boxplot(TFC_percent_atkdef[i], positions=[positions_atkdef[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="orange"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[positions_atk[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atkdef[i], positions=[positions_atkdef[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="orange"))

    # Trend lines
    axes[0].plot(trend_positions_atk, [np.mean(data) for data in TFC_percent_atk], color="cyan", marker='o', label='Attack Only')
    axes[0].plot(trend_positions_atkdef, [np.mean(data) for data in TFC_percent_atkdef], color="orange", marker='o', label='Attack with Defense')
    axes[1].plot(trend_positions_atk, [np.mean(data) for data in Cap_percent_atk], color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions_atkdef, [np.mean(data) for data in Cap_percent_atkdef], color="orange", marker='o', label='Attack with Defense')

    # Axes labels and legends
    axes[0].set_xticks((positions_atk + positions_atkdef) / 2)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_ylabel('Total Food Collected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend()
    axes[1].set_xlabel('Pheromone Lay Rate (%)', fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Robots Captured (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axes[1].tick_params(axis='y', labelsize=y_tick_fontsize)
    # axes[1].legend()

    plt.tight_layout()
    plt.savefig('./results/Exp_AtkDef_varyLayRate.png')

def PlotExp_AtkDef_varyDetractorPercentage():

    # params
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24
    
    # get all filenames in directory for attack only
    flist_atk = []
    for filename in os.listdir("./results/results_Exp1_noDef_r24_st2700_30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_atk.append(os.path.join("./results/results_Exp1_noDef_r24_st2700_30it", filename))
        else:
            continue

    # get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/results_Exp1_r24_st2700_30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/results_Exp1_r24_st2700_30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_atk.sort(key=extract_d_value)
    flist_atkdef.sort(key=extract_d_value)

    print(flist_atk)
    print(flist_atkdef)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_atk:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))
    
    TFClist_atkdef = []
    Caplist_atkdef = []
    for filename in flist_atkdef:
        Read(filename)
        TFClist_atkdef.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atkdef.append(np.array(ROBOTS_CAPTURED).astype(int))
    
    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / (total_robots * 0.75)) * 100 for data in Caplist_atk] # 25% are detractors, so 75% are normal agents
    TFC_percent_atkdef = [(data / total_food) * 100 for data in TFClist_atkdef]
    Cap_percent_atkdef = [(data / (total_robots * 0.75)) * 100 for data in Caplist_atkdef] # 25% are detractors, so 75% are normal agents

    # lay rates
    lay_rates = ["0", "10", "20", "30", "40" , "50"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

    # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    positions_atk = np.arange(1, 2*num_rates, step=2)
    positions_atkdef = positions_atk + width + gap

    # Calculate positions for trend lines
    trend_positions_atk = positions_atk + width / 2
    trend_positions_atkdef = positions_atkdef + width / 2

    # Plot boxplots and trend lines
    for i in range(num_rates):
        # Boxplots
        axes[0].boxplot(TFC_percent_atk[i], positions=[positions_atk[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[0].boxplot(TFC_percent_atkdef[i], positions=[positions_atkdef[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="orange"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[positions_atk[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atkdef[i], positions=[positions_atkdef[i]], widths=width, patch_artist=True, boxprops=dict(facecolor="orange"))

    # Trend lines
    axes[0].plot(trend_positions_atk, [np.mean(data) for data in TFC_percent_atk], color="cyan", marker='o', label='Attack Only')
    axes[0].plot(trend_positions_atkdef, [np.mean(data) for data in TFC_percent_atkdef], color="orange", marker='o', label='Attack with Defense')
    axes[1].plot(trend_positions_atk, [np.mean(data) for data in Cap_percent_atk], color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions_atkdef, [np.mean(data) for data in Cap_percent_atkdef], color="orange", marker='o', label='Attack with Defense')

    # Axes labels and legends
    axes[0].set_xticks((positions_atk + positions_atkdef) / 2)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_ylabel('Total Food Collected (%)')
    axes[0].legend()
    axes[1].set_xlabel('Detractor Percentage (%)')
    axes[1].set_ylabel('Total Robots Captured (%)')
    # axes[1].legend()

    plt.tight_layout()
    plt.savefig('./results/Exp_AtkDef_varyDetractorPercentage.png')

def PlotExp_DefOnly_varyDetractorPercentage():
    # Params
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24
    
    # Get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/results_Exp6_r24_st2700_30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/results_Exp6_r24_st2700_30it", filename))

    # Sort the filenames based on the extracted d value
    flist_atkdef.sort(key=extract_d_value)

    # Parse data from files
    IsoDetlist_def = []
    IsoForlist_def = []
    for filename in flist_atkdef:
        Read(filename)
        IsoDetlist_def.append(np.array(TOTAL_ISOLATED_DETRACTORS).astype(int))
        IsoForlist_def.append(np.array(TOTAL_ISOLATED_FORAGERS).astype(int))
    
    # Detractor percentages
    detractor_percentages = ["0", "10", "20", "30", "40", "50"]
    det_perc = [0, 0.10, 0.20, 0.30, 0.40, 0.50]
    num_rates = len(detractor_percentages)

    # # Calculate percentages (25% are detractors so 75% are normal agents)
    # IsoDet_percent_def = []      # detractors isolated
    # IsoFor_percent_def = []      # foragers (normal agents) captured

    # for Ddata, Fdata, p in zip(IsoDetlist_def, IsoForlist_def, det_perc):
    #     if p != 0:
    #         IsoDet_percent_def.append((Ddata / (total_robots * p)) * 100)
    #     else:
    #         IsoDet_percent_def.append(100)  # We will say that 100% of the detractors are isolated if there are none
    #     IsoFor_percent_def.append((Fdata / (total_robots * (1-p))) * 100)

    # Calculate percentages (number of normal agents stays the same. Detractors increase as a percentage of the normal agents. The total number of robots increases as a result.)
    IsoDet_percent_def = []      # detractors isolated
    IsoFor_percent_def = []      # foragers (normal agents) captured

    for Ddata, Fdata, p in zip(IsoDetlist_def, IsoForlist_def, det_perc):
        IsoDet_percent_def.append((Ddata / (total_robots * p)) * 100)
        IsoFor_percent_def.append((Fdata / total_robots) * 100)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate positions for boxplots
    width = 0.15  # Boxplot width
    gap = 0.05  # Gap between boxplots
    base_positions = np.arange(1, num_rates + 1)  # Base positions for each detractor percentage
    positions_Iso = base_positions - width/2 - gap/2
    positions_FP = base_positions + width/2 + gap/2

    # Plot boxplots
    box_TFC = ax.boxplot(IsoDet_percent_def, positions=positions_Iso, widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
    box_Cap = ax.boxplot(IsoFor_percent_def, positions=positions_FP, widths=width, patch_artist=True, boxprops=dict(facecolor="orange"))

    # Plot trend lines
    mean_IsoDet_def = [np.mean(data) for data in IsoDet_percent_def]
    mean_IsoFor_def = [np.mean(data) for data in IsoFor_percent_def]

    ax.plot(positions_Iso, mean_IsoDet_def, color="cyan", marker='o', label='Isolated Detractors Trend')
    ax.plot(positions_FP, mean_IsoFor_def, color="orange", marker='o', label='Isolted Foragers Trend')

    # Set x-ticks to the middle of each group of box plots
    ax.set_xticks(base_positions)
    ax.set_xticklabels(detractor_percentages)

    # Axes labels and legend
    ax.set_xlabel('Detractor Percentage (%)')
    ax.set_ylabel('Isolated Robots (%)')
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig('./results/sim_time_1800/Exp_DefOnly_varyDetractorPercentage.png')

def extract_rlp_value(filename):
    """
    Extract the rlp value from the filename.
    Assumes the filename contains 'rlp' followed by a number (e.g., 'rlp8.0').
    """
    match = re.search(r"rlp(\d+\.\d+)", filename)
    if match:
        return float(match.group(1))
    else:
        return 0  # Default value if 'rlp' is not found
    
def extract_d_value(filename):
    """
    Extracts the 'd' value from the filename.

    Args:
    filename (str): The filename from which to extract the 'd' value.

    Returns:
    float: The extracted 'd' value.
    """
    match = re.search(r"_d(\d+)", filename)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("No 'd' value found in filename.")

def plot_experiment(flist, rdpath, total_robots, total_food):
    """
    This function plots multi-box plots with trend lines.

    flist: List of filenames containing experiment data.
    rdpath: Directory path where the plot will be saved.
    total_robots: Total number of robots in the experiment.
    total_food: Total amount of food in the experiment.
    """
    # Read and process the data
    TFC_percent, Cap_percent = process_data(flist, total_robots, total_food)

    # Calculate mean and standard deviation for the percentages
    TFCdata = [(round(np.mean(data), 1), np.std(data)) for data in TFC_percent]
    Capdata = [(round(np.mean(data), 1), np.std(data)) for data in Cap_percent]

    # Create the boxplot data
    boxplot_data_TFC = [data for data in TFC_percent]
    boxplot_data_Cap = [data for data in Cap_percent]

    # Create a figure with two subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    # Plot for Total Food Collected
    plot_with_trend(axs[0], boxplot_data_TFC, TFCdata, 'Resources Collected (%)', 'blue')

    # Plot for Robots Captured
    plot_with_trend(axs[1], boxplot_data_Cap, Capdata, 'Robots Captured (%)', 'red')

    # Set labels and save the plot
    axs[1].set_xlabel('Travel Time Tolerance (%)', fontsize=24, labelpad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(rdpath, 'Experiment5_boxplot_trends.png'))
    plt.clf()

def process_data(flist, total_robots, total_food):
    """
    Processes the data files and returns the percentage of total food collected and robots captured.
    """
    # Initialize lists to store data
    TFClist, Caplist = [], []

    # Read data from each file
    for filename in flist:
        # Your function to read data from files
        # Read(filename)
        # Simulate data for example
        TFClist.append(np.random.rand(20) * total_food)
        Caplist.append(np.random.rand(20) * total_robots)

    # Calculate percentages
    TFC_percent = [(data / total_food) * 100 for data in TFClist]
    Cap_percent = [(data / (total_robots * 0.75)) * 100 for data in Caplist]

    return TFC_percent, Cap_percent

def plot_with_trend(ax, boxplot_data, mean_std_data, ylabel, color):
    """
    Plots a box plot with a trend line.
    """
    ax.boxplot(boxplot_data, patch_artist=True)
    means = [data[0] for data in mean_std_data]
    stds = [data[1] for data in mean_std_data]
    ax.errorbar(range(1, len(means)+1), means, yerr=stds, fmt='o-', label=ylabel, color=color, capsize=5, alpha=0.7, linewidth=2)
    ax.set_ylabel(ylabel, fontsize=24, labelpad=15)
    ax.grid(True)
    ax.tick_params(axis='y', labelsize=18)

if __name__ == "__main__":

    # PlotExp_AtkDef_varyLayRate()
    PlotExp_AtkDef_varyDetractorPercentage()
    PlotExp_DefOnly_varyDetractorPercentage()
















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
