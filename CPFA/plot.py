import xml_config as config
import os, time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
FORAGER_FOOD_COLLECTED = []
DETRACTOR_FOOD_COLLECTED = []
FINAL_UNIVELOSITY = []

TIME_IN_SECONDS = []
REAL_PTRAILS_PER10SECS = []
FAKE_PTRAILS_PER10SECS = []

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
    FORAGER_FOOD_COLLECTED.clear()
    DETRACTOR_FOOD_COLLECTED.clear()
    FINAL_UNIVELOSITY.clear()
    
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
            FORAGER_FOOD_COLLECTED.append(data[13])
            DETRACTOR_FOOD_COLLECTED.append(data[14])
            FINAL_UNIVELOSITY.append(data[15])

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

def ReadTrailRatio(fname):
    count = 0
    TIME_IN_SECONDS.clear()
    REAL_PTRAILS_PER10SECS.clear()
    FAKE_PTRAILS_PER10SECS.clear()
    
    with open(fname) as f:
        for line in f.readlines():
            data = line.strip().split(',')
            if data[0] == 'Time (seconds)':
                continue
            TIME_IN_SECONDS.append(data[0])
            REAL_PTRAILS_PER10SECS.append(data[1])
            FAKE_PTRAILS_PER10SECS.append(data[2])

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
    for filename in os.listdir("./results/results_layrate_NEW/results_analysis4_r24_1800_rc30it"):
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
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

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
    total_robots = 32
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24
    
    # get all filenames in directory for attack only
    flist_atk = []
    for filename in os.listdir("./results/results_Exp6_noDef_r24_st2700_30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_atk.append(os.path.join("./results/results_Exp6_noDef_r24_st2700_30it", filename))
        else:
            continue

    # get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/results_Exp6_r24_st2700_30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/results_Exp6_r24_st2700_30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_atk.sort(key=extract_d_value)
    flist_atkdef.sort(key=extract_d_value)

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
   
    # detractor percentages
    det_percents = ["0", "10", "20", "30", "40" , "50"]
    det_perc_calc = [0.0, 0.10, 0.20, 0.30, 0.40, 0.50]
    num_percents = len(det_percents)
    
    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / (total_robots*(1+p))) * 100 for p,data in zip(det_perc_calc, Caplist_atk)] 
    TFC_percent_atkdef = [(data / total_food) * 100 for data in TFClist_atkdef]
    Cap_percent_atkdef = [(data / (total_robots*(1+p))) * 100 for p,data in zip(det_perc_calc,Caplist_atkdef)] 

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

    # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    positions_atk = np.arange(1, 2*num_percents, step=2)
    positions_atkdef = positions_atk + width + gap

    # Calculate positions for trend lines
    trend_positions_atk = positions_atk + width / 2
    trend_positions_atkdef = positions_atkdef + width / 2

    # Plot boxplots and trend lines
    for i in range(num_percents):
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
    axes[0].set_xticklabels(det_percents)
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
    for filename in os.listdir("./results/sim_time_1800/results_Exp6_new_r24_detpercent_st1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/sim_time_1800/results_Exp6_new_r24_detpercent_st1800_rc30it", filename))

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

    ## Calculate percentages
    IsoDet_percent_def = []  # detractors isolated
    IsoFor_percent_def = []  # foragers (normal agents) captured

    for Ddata, Fdata, p in zip(IsoDetlist_def, IsoForlist_def, det_perc):
        # Calculate the total number of robots in each simulation
        total_detractors = int(total_robots * p)
        total_robots_in_simulation = total_robots + total_detractors

        # Calculate percentage of isolated detractors
        if total_detractors > 0:
            IsoDet_percent_def.append((Ddata / total_detractors) * 100)
        else:
            IsoDet_percent_def.append(0)  # No detractors to be isolated when p is 0

        # Calculate percentage of isolated foragers
        if total_robots_in_simulation > 0:
            IsoFor_percent_def.append((Fdata / total_robots_in_simulation) * 100)
        else:
            IsoFor_percent_def.append(0)  # No robots to be captured when total robots is 0



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
    plt.savefig('./results/Exp_DefOnly_varyDetractorPercentage.png')

def PlotExp_DefOnly_performanceEval():
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
    for filename in os.listdir("./results/results_Exp7_r24_st2700_30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results//results_Exp7_r24_st2700_30it", filename))

    # Sort the filenames based on the extracted d value
    flist_atkdef.sort(key=extract_d_value)

    # Parse data from files
    Foragerlist = []
    Detractorlist = []
    for filename in flist_atkdef:
        Read(filename)
        Foragerlist.append(np.array(FORAGER_FOOD_COLLECTED).astype(int))
        Detractorlist.append(np.array(DETRACTOR_FOOD_COLLECTED).astype(int))
    
    # Detractor percentages
    detractor_percentages = ["0", "10", "20", "30", "40", "50"]
    det_perc = [0, 0.10, 0.20, 0.30, 0.40, 0.50]
    num_rates = len(detractor_percentages)

    ## Calculate percentages
    Forager_performance = []  # forager food collected
    Detractor_performance = []  # detractor food collected

    for Fdata, Ddata in zip(Foragerlist, Detractorlist):
        
        # Calculate percentage of forager food collected
        Forager_performance.append((Fdata / total_food) * 100)

        # Calculate percentage of detractor food collected
        Detractor_performance.append((Ddata / total_food) * 100)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate positions for boxplots
    width = 0.15  # Boxplot width
    gap = 0.05  # Gap between boxplots
    base_positions = np.arange(1, num_rates + 1)  # Base positions for each detractor percentage
    positions_Iso = base_positions - width/2 - gap/2
    positions_FP = base_positions + width/2 + gap/2

    # Plot boxplots
    box_TFC = ax.boxplot(Forager_performance, positions=positions_Iso, widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
    box_Cap = ax.boxplot(Detractor_performance, positions=positions_FP, widths=width, patch_artist=True, boxprops=dict(facecolor="orange"))

    # Plot trend lines
    mean_Forager_perf = [np.mean(data) for data in Forager_performance]
    mean_Detractor_perf = [np.mean(data) for data in Detractor_performance]

    ax.plot(positions_Iso, mean_Forager_perf, color="cyan", marker='o', label='Forager Performance Trend')
    ax.plot(positions_FP, mean_Detractor_perf, color="orange", marker='o', label='Detractor Performance Trend')

    # Set x-ticks to the middle of each group of box plots
    ax.set_xticks(base_positions)
    ax.set_xticklabels(detractor_percentages)

    # Axes labels and legend
    ax.set_xlabel('Detractor Percentage (%)')
    ax.set_ylabel('Resources Collected (%)')
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig('./results/Exp_DefOnly_performanceEval.png')

def PlotAnalysis1_st1800():
    total_robots = 32
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # get all filenames in directory for attack only
    flist_attackData = []
    for filename in os.listdir("./results/analysis_12-14-23/results_analysis1_r24_1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_attackData.append(os.path.join("./results/analysis_12-14-23/results_analysis1_r24_1800_rc30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_attackData.sort(key=extract_rlp_value)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # lay rates
    lay_rates = ["1.0", "4.0", "8.0", "12.0"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

   # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    num_lay_rates = len(lay_rates)
    positions = np.arange(1, num_lay_rates * 2, step=2)

    # Prepare data for trend lines
    trend_positions = positions
    mean_TFC_percent_atk = [np.mean(data) for data in TFC_percent_atk]
    mean_Cap_percent_atk = [np.mean(data) for data in Cap_percent_atk]

    # Plot boxplots
    for i, position in enumerate(positions):
        # Boxplots
        box_pos = position
        axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))

    # Plot trend lines
    axes[0].plot(trend_positions, mean_TFC_percent_atk, color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions, mean_Cap_percent_atk, color="cyan", marker='o', label='Attack Only')
    
    # Set y-ticks
    axes[0].set_yticks(np.arange(40, 101, 10))  # Y-ticks from 0 to 100, increment by 10s
    axes[1].set_yticks(np.arange(0, 101, 20))
    
    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_ylabel('Total Food\nCollected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend()
    axes[1].set_xlabel('Pheromone Lay Rate (%)', fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Robots\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=15)
    
    # Uniform tick sizes
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)

    # Adjust layout
    plt.tight_layout(pad=2.0)  # Added padding to layout adjustment

    # Save the plot
    plt.savefig('./results/analysis_12-14-23/results_analysis1_r24_1800_rc30it/dExp_AtkOnly_varyLayRate.png')

def PlotAnalysis1_st2700():
    total_robots = 32
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # get all filenames in directory for attack only
    flist_attackData = []
    for filename in os.listdir("./results/analysis_12-14-23/results_analysis1_r24_2700_rc30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_attackData.append(os.path.join("./results/analysis_12-14-23/results_analysis1_r24_2700_rc30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_attackData.sort(key=extract_rlp_value)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # lay rates
    lay_rates = ["1.0", "4.0", "8.0", "12.0"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

   # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    num_lay_rates = len(lay_rates)
    positions = np.arange(1, num_lay_rates * 2, step=2)

    # Prepare data for trend lines
    trend_positions = positions
    mean_TFC_percent_atk = [np.mean(data) for data in TFC_percent_atk]
    mean_Cap_percent_atk = [np.mean(data) for data in Cap_percent_atk]

    # Plot boxplots
    for i, position in enumerate(positions):
        # Boxplots
        box_pos = position
        axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))

    # Plot trend lines
    axes[0].plot(trend_positions, mean_TFC_percent_atk, color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions, mean_Cap_percent_atk, color="cyan", marker='o', label='Attack Only')
    
    # Set y-ticks
    axes[0].set_yticks(np.arange(40, 101, 10))  # Y-ticks from 0 to 100, increment by 10s
    axes[1].set_yticks(np.arange(0, 101, 20))
    
    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_ylabel('Total Food\nCollected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend()
    axes[1].set_xlabel('Pheromone Lay Rate (%)', fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Robots\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=15)
    
    # Uniform tick sizes
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)

    # Adjust layout
    plt.tight_layout(pad=2.0)  # Added padding to layout adjustment

    # Save the plot
    plt.savefig('./results/analysis_12-14-23/results_analysis1_r24_2700_rc30it/dExp_AtkOnly_varyLayRate.png')

def PlotAnalysis1_NotLetDetractorsUseMLT():
    total_robots = 32
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # get all filenames in directory for attack only
    flist_attackData = []
    for filename in os.listdir("./results/analysis_12-14-23/results_analysis1_NotLetDetUseMLT_r24_2700_rc30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_attackData.append(os.path.join("./results/analysis_12-14-23/results_analysis1_NotLetDetUseMLT_r24_2700_rc30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_attackData.sort(key=extract_rlp_value)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # lay rates
    lay_rates = ["1.0", "4.0", "8.0", "12.0"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

   # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    num_lay_rates = len(lay_rates)
    positions = np.arange(1, num_lay_rates * 2, step=2)

    # Prepare data for trend lines
    trend_positions = positions
    mean_TFC_percent_atk = [np.mean(data) for data in TFC_percent_atk]
    mean_Cap_percent_atk = [np.mean(data) for data in Cap_percent_atk]

    # Plot boxplots
    for i, position in enumerate(positions):
        # Boxplots
        box_pos = position
        axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))

    # Plot trend lines
    axes[0].plot(trend_positions, mean_TFC_percent_atk, color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions, mean_Cap_percent_atk, color="cyan", marker='o', label='Attack Only')
    
    # Set y-ticks
    axes[0].set_yticks(np.arange(40, 101, 10))  # Y-ticks from 0 to 100, increment by 10s
    axes[1].set_yticks(np.arange(0, 101, 20))
    
    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_ylabel('Total Food\nCollected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend()
    axes[1].set_xlabel('Pheromone Lay Rate (%)', fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Robots\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=15)
    
    # Uniform tick sizes
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)

    # Adjust layout
    plt.tight_layout(pad=2.0)  # Added padding to layout adjustment

    # Save the plot
    plt.savefig('./results/analysis_12-14-23/results_analysis1_NotLetDetUseMLT_r24_2700_rc30it/dExp_AtkOnly_varyLayRate.png')

def PlotAnalysis2_NotLetDetractorsUseMLT():
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # get all filenames in directory for attack only
    flist_attackData = []
    for filename in os.listdir("./results/analysis_12-18-23/results_analysis2_r24_1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_attackData.append(os.path.join("./results/analysis_12-18-23/results_analysis2_r24_1800_rc30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_attackData.sort(key=extract_rlp_value)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # lay rates
    lay_rates = ["1.0", "4.0", "8.0", "12.0"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

   # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    num_lay_rates = len(lay_rates)
    positions = np.arange(1, num_lay_rates * 2, step=2)

    # Prepare data for trend lines
    trend_positions = positions
    mean_TFC_percent_atk = [np.mean(data) for data in TFC_percent_atk]
    mean_Cap_percent_atk = [np.mean(data) for data in Cap_percent_atk]

    # Plot boxplots
    for i, position in enumerate(positions):
        # Boxplots
        box_pos = position
        axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))

    # Plot trend lines
    axes[0].plot(trend_positions, mean_TFC_percent_atk, color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions, mean_Cap_percent_atk, color="cyan", marker='o', label='Attack Only')
    
    # Set y-ticks
    axes[0].set_yticks(np.arange(40, 101, 10))  # Y-ticks from 0 to 100, increment by 10s
    axes[1].set_yticks(np.arange(0, 101, 20))
    
    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_ylabel('Total Food\nCollected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend()
    axes[1].set_xlabel('Pheromone Lay Rate (%)', fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Robots\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=15)
    
    # Uniform tick sizes
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)

    # Adjust layout
    plt.tight_layout(pad=2.0)  # Added padding to layout adjustment

    # Save the plot
    plt.savefig('./results/analysis_12-18-23/results_analysis2_r24_1800_rc30it/dExp_AtkOnly_varyLayRate.png')

def PlotAnalysis4():
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # get all filenames in directory for attack only
    flist_attackData = []
    for filename in os.listdir("./results/analysis_layrate_NEW/results_analysis4_r24_1800_rc30it"):
        if filename.endswith("RatioCheck.txt"):
            flist_attackData.append(os.path.join("./results/analysis_12-21-23/results_analysis4_r32_1800_rc30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_attackData.sort(key=extract_rlp_value)

    # Initialize the 3D list structure for ratio data
    lay_rates = ["1.0", "4.0", "8.0", "12.0"]
    ratio_data = [[[] for _ in range(30)] for _ in range(len(lay_rates))]  # 4 lay rates, 30 simulations each

    for i, filename in enumerate(flist_attackData):
        ReadTrailRatio(filename)

        # Initialize a new list for each simulation's data
        simulation_data = [[] for _ in range(30)]
        simulation_index = 0

        for st, rt, ft in zip(TIME_IN_SECONDS, REAL_PTRAILS_PER10SECS, FAKE_PTRAILS_PER10SECS):
            if st == '10' and simulation_data[simulation_index]:  # Start of a new simulation
                simulation_index += 1  # Move to the next simulation

            # Ensure the index is within range
            if simulation_index < 30:
                rt_int = int(rt) if rt.isdigit() else 0
                ft_int = int(ft) if ft.isdigit() else 0
                ratio = rt_int / (ft_int + 0.0001)  # Calculate ratio
                simulation_data[simulation_index].append(ratio)

        # Assign the parsed data to the appropriate lay rate in ratio_data
        ratio_data[i] = simulation_data

    # Print the structure to check if it's correct
    for i, lay_rate_data in enumerate(ratio_data):
        print(f"Lay Rate {lay_rates[i]}: {len(lay_rate_data)} simulations")
        for j, sim in enumerate(lay_rate_data):
            print(f"  Simulation {j+1}: {len(sim)} time points")

    # Plotting setup
    fig, axes = plt.subplots(nrows=len(lay_rates), ncols=1, figsize=(15, 10), sharex=True)

    # Plotting for each lay rate
    for i, lay_rate in enumerate(lay_rates):
        if not ratio_data[i]:
            print(f"No data for lay rate {lay_rate}. Skipping this plot.")
            continue

        # Find the minimum length of simulations for the current lay rate
        min_simulation_length = min(len(sim_data) for sim_data in ratio_data[i] if sim_data)

        if min_simulation_length == 0:
            print(f"No time points data for lay rate {lay_rate}. Skipping this plot.")
            continue

        step = 10  # Plot every 10th time point
        positions = np.arange(0, min_simulation_length, step)
        data_for_boxplot = [[sim_data[time_point] for sim_data in ratio_data[i] if len(sim_data) > time_point] for time_point in positions]
        mean_ratios = [np.mean(time_point_data) for time_point_data in data_for_boxplot]

        # Plot boxplots and trend lines
        axes[i].boxplot(data_for_boxplot, positions=positions, widths=2, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[i].plot(positions, mean_ratios, color="cyan", marker='o', label=f'Lay Rate {lay_rate}')

        # Dynamically determine y-axis limits
        all_data_points = [item for sublist in data_for_boxplot for item in sublist]
        y_min, y_max = min(all_data_points), max(all_data_points)
        axes[i].set_ylim([y_min - 0.1 * abs(y_min), y_max + 0.1 * abs(y_max)])  # Add 10% buffer

        # Set y-axis label
        axes[i].set_ylabel(f'Ratio at Lay Rate {lay_rate}', fontsize=12)
        axes[i].legend()

        # Adjust x-ticks
        axes[i].set_xticks(positions)
        axes[i].set_xticklabels([str(int(p)) for p in positions], rotation=45, ha="right")

    # X-axis labels
    axes[-1].set_xlabel('Time (seconds)', fontsize=12)

    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('./results/TrailRatioAnalysis.png')

    # Call the function with your data
    print_data_summary(ratio_data, lay_rates)

def PlotAnalysis3():
    total_robots = 32
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

   # Calculate positions for boxplots# get all filenames in directory for attack only
    flist_atk = []
    for filename in os.listdir("./results/analysis_12-18-23/results_analysis3_noAtk_r32_1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_atk.append(os.path.join("./results/analysis_12-18-23/results_analysis3_noAtk_r32_1800_rc30it", filename))
        else:
            continue

    # get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/analysis_12-18-23/results_analysis3_r32_1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/analysis_12-18-23/results_analysis3_r32_1800_rc30it", filename))
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
    Cap_percent_atk = [(data / (total_robots)) * 100 for data in Caplist_atk] # 25% are detractors, so 75% are normal agents
    TFC_percent_atkdef = [(data / total_food) * 100 for data in TFClist_atkdef]
    Cap_percent_atkdef = [(data / (total_robots)) * 100 for data in Caplist_atkdef] # 25% are detractors, so 75% are normal agents

    # lay rates
    lay_rates = ["1.0", "4.0", "8.0", "12.0"]
    num_rates = len(lay_rates)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

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
    axes[0].plot(trend_positions_atk, [np.mean(data) for data in TFC_percent_atk], color="cyan", marker='o', label='No Attack')
    axes[0].plot(trend_positions_atkdef, [np.mean(data) for data in TFC_percent_atkdef], color="orange", marker='o', label='Misleading Trail Attack')
    axes[1].plot(trend_positions_atk, [np.mean(data) for data in Cap_percent_atk], color="cyan", marker='o', label='No Attack')
    axes[1].plot(trend_positions_atkdef, [np.mean(data) for data in Cap_percent_atkdef], color="orange", marker='o', label='Misleading Trail Attack')

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
    plt.savefig('./results/analysis_12-18-23/results_analysis3_noAtk_r32_1800_rc30it/Analysis3_varyLayRate.png')

def Output_IncreaseTrails_layrate(output_file):
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # Define lay rates and get all filenames in directory for attack only
    lay_rates = ["1", "4", "8", "12"]
    flist_attackData = []
    for filename in os.listdir("./results/analysis_layrate_MLT/results_analysis4_r24_1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            flist_attackData.append(os.path.join("./results/analysis_layrate_MLT/results_analysis4_r24_1800_rc30it", filename))

    # Sort the filenames based on lay rates
    flist_attackData.sort(key=extract_rlp_value)  # Use an appropriate function to extract lay rate values

    # Parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)  # Ensure Read2 function processes the file correctly
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    with open(output_file, 'w') as out_file:
        for i, lay_rate in enumerate(lay_rates):
            out_file.write(f"Global Lay Rate: {lay_rate}\n")
            out_file.write("Total Resources Collected (%):\n")
            out_file.write(f"  Mean: {np.mean(TFC_percent_atk[i])}%\n")
            out_file.write(f"  Median: {np.median(TFC_percent_atk[i])}%\n")
            out_file.write(f"  Min: {np.min(TFC_percent_atk[i])}%\n")
            out_file.write(f"  Max: {np.max(TFC_percent_atk[i])}%\n")
            out_file.write(f"  StdDev: {np.std(TFC_percent_atk[i])}%\n")
            out_file.write("Total Foragers Captured (%):\n")
            out_file.write(f"  Mean: {np.mean(Cap_percent_atk[i])}%\n")
            out_file.write(f"  Median: {np.median(Cap_percent_atk[i])}%\n")
            out_file.write(f"  Min: {np.min(Cap_percent_atk[i])}%\n")
            out_file.write(f"  Max: {np.max(Cap_percent_atk[i])}%\n")
            out_file.write(f"  StdDev: {np.std(Cap_percent_atk[i])}%\n")
            out_file.write("-------------------------------------------\n")

def PlotAnalysis_IncreaseTrails():
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24

    # get all filenames in directory for attack only
    flist_attackData = []
    # for filename in os.listdir("./results/results_IncreaseTrails_r24_rlp4_st1800_30it"):
    for filename in os.listdir("./results/results_RateIncrease_DEF_r24_rlpf6_rlpd1_st1800_30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            # flist_attackData.append(os.path.join("./results/results_IncreaseTrails_r24_rlp4_st1800_30it", filename))
            flist_attackData.append(os.path.join("./results/results_RateIncrease_DEF_r24_rlpf6_rlpd1_st1800_30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_attackData.sort(key=extract_d_value)

    # parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # Detractor percentages
    detractor_percentages = ["0", "10", "20", "30", "40", "50"]
    det_perc = [0, 0.10, 0.20, 0.30, 0.40, 0.50]
    num_rates = len(detractor_percentages)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)

   # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.35  # Boxplot width
    num_lay_rates = len(detractor_percentages)
    positions = np.arange(1, num_lay_rates * 2, step=2)

    # Prepare data for trend lines
    trend_positions = positions
    mean_TFC_percent_atk = [np.mean(data) for data in TFC_percent_atk]
    mean_Cap_percent_atk = [np.mean(data) for data in Cap_percent_atk]

    # Plot boxplots
    for i, position in enumerate(positions):
        # Boxplots
        box_pos = position
        axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))

    # Plot trend lines
    axes[0].plot(trend_positions, mean_TFC_percent_atk, color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions, mean_Cap_percent_atk, color="cyan", marker='o', label='Attack Only')
    
    # Set y-ticks
    axes[0].set_yticks(np.arange(0, 101, 20))  # Y-ticks from 0 to 100, increment by 10s
    axes[1].set_yticks(np.arange(0, 101, 20))
    
    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(detractor_percentages)
    axes[0].set_ylabel('Total Food\nCollected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend()
    axes[1].set_xlabel('Detractor Percentage (%)', fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Robots\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=15)
    
    # Uniform tick sizes
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)

    # Adjust layout
    plt.tight_layout(pad=2.0)  # Added padding to layout adjustment

    # Save the plot
    # plt.savefig('./results/results_IncreaseTrails_r24_rlp4_st1800_30it/PlotAnalysis_IncreaseTrails.png')
    plt.savefig('./results/results_RateIncrease_DEF_r24_rlpf6_rlpd1_st1800_30it/PlotAnalysis_IncreaseTrails.png')




############################################################################################
'''
PlotAnalysis_IncreaseTrails_layrate() was used to generate the plot for Experiment 1 (figure 4) 
in the paper "Detection and Mitigation of Misleading Pheromone Trails in Foraging Robot Swarms"
'''
############################################################################################
def PlotAnalysis_VaryNumCylinderObstacles_AtkDef():
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 24
    y_tick_fontsize = 24
    xlabel_fontsize = 28
    ylabel_fontsize = 28
    legend_fontsize = 18

    # Define lay rates and get all filenames in directory for attack only
    num_cylinder_obstacles = ["0", "4", "8", "12", "16"]
    flist_attackData = []
    for filename in os.listdir("./results/resultsExp10-2_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it"):
    # for filename in os.listdir("./results/resultsExp10-3_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it"):
        if filename.endswith("AttackData.txt"):
            flist_attackData.append(os.path.join("./results/resultsExp10-2_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it", filename))
            # flist_attackData.append(os.path.join("./results/resultsExp10-3_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it", filename))
    # Sort the filenames based on lay rates
    flist_attackData.sort(key=extract_ncobs_value)  # Use an appropriate function to extract lay rate values

    # Parse data from files
    TFClist_atk = []
    Caplist_atk = []
    NFPlist_atk = []
    UVlist_atk = []
    for filename in flist_attackData:
        Read(filename)  # Ensure Read2 function processes the file correctly
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))
        NFPlist_atk.append(np.array(NUM_FALSE_POSITIVES).astype(int))
        UVlist_atk.append(np.array(FINAL_UNIVELOSITY).astype(float))

    # Calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # Plotting
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 16), sharex=True)

    # Calculate positions for boxplots
    gap = 0.5
    width = 0.35
    lengthof_num_cylinder_obstacles = len(num_cylinder_obstacles)
    positions = np.arange(1, lengthof_num_cylinder_obstacles * 2, step=2)

    # Plot boxplots and trend lines
    for i in range(lengthof_num_cylinder_obstacles):
        box_pos = positions[i]
        if (len(TFC_percent_atk[i]) > 0):
            axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        else:
            print("TFC_percent_atk[i] is 0")
        if (len(Cap_percent_atk[i]) > 0):
            axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        else:
            print("Cap_percent_atk[i] is 0")
        if (len(NFPlist_atk[i]) > 0):
            axes[2].boxplot(NFPlist_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        else:
            print("NFPlist_atk[i] is 0")
        if (len(UVlist_atk[i]) > 0):
            axes[3].boxplot(UVlist_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        else:
            print("UVlist_atk[i] is 0")

    # Plot trend lines
    trend_positions = np.array(positions) + width / 2
    axes[0].plot(trend_positions, [np.mean(data) for data in TFC_percent_atk], color="cyan", marker='o', label='Attack + Def')
    axes[1].plot(trend_positions, [np.mean(data) for data in Cap_percent_atk], color="cyan", marker='o', label='Attack + Def')
    axes[2].plot(trend_positions, [np.mean(data) for data in NFPlist_atk], color="cyan", marker='o', label='Attack + Def')
    axes[3].plot(trend_positions, [np.mean(data) for data in UVlist_atk], color="cyan", marker='o', label='Attack + Def')

    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(num_cylinder_obstacles)
    axes[0].set_yticks(np.arange(20, 101, 20))
    axes[0].set_ylabel('Total Resources\nCollected (%)', fontsize=ylabel_fontsize, labelpad=50, rotation=67.5)
    axes[0].legend(fontsize=legend_fontsize)
    axes[1].set_ylabel('Total Foragers\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=50, rotation=67.5)
    axes[2].set_ylabel('False Positives\nDetected', fontsize=ylabel_fontsize, labelpad=50, rotation=67.5)
    axes[3].set_ylabel('Final Univelocity', fontsize=ylabel_fontsize, labelpad=50, rotation=67.5)
    axes[3].set_xlabel("Number of Cylinder Obstacles", fontsize=xlabel_fontsize, labelpad=15)

    # Uniform tick sizes and adjust layout
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)
    plt.tight_layout(pad=2.0)

    # Save the plot
    plt.savefig('./results/resultsExp10-2_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it/PlotAnalysis_VaryNumCylinderObstacles.png')
    # plt.savefig('./results/resultsExp10-3_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it/PlotAnalysis_VaryNumCylinderObstacles.png')
    # Open a file to write the results
    with open('./results/resultsExp10-2_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it/AnalysisSummary.txt', 'w') as outfile:
    # with open('./results/resultsExp10-3_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_60it/AnalysisSummary.txt', 'w') as outfile:
        outfile.write("Summary of Experiment Results\n")
        outfile.write("----------------------------\n")
        outfile.write("Number of Cylinder Obstacles | Total Resources Collected (%) Mean (Std Dev) | Total Foragers Captured (%) Mean (Std Dev) | False Positives Detected Mean (Std Dev) | Final Univelocity Mean (Std Dev)\n")
        outfile.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
        
        for i, n_obs in enumerate(num_cylinder_obstacles):
            mean_TFC = np.mean(TFC_percent_atk[i]) if len(TFC_percent_atk[i]) > 0 else "N/A"
            std_TFC = np.std(TFC_percent_atk[i]) if len(TFC_percent_atk[i]) > 0 else "N/A"
            mean_Cap = np.mean(Cap_percent_atk[i]) if len(Cap_percent_atk[i]) > 0 else "N/A"
            std_Cap = np.std(Cap_percent_atk[i]) if len(Cap_percent_atk[i]) > 0 else "N/A"
            mean_NFP = np.mean(NFPlist_atk[i]) if len(NFPlist_atk[i]) > 0 else "N/A"
            std_NFP = np.std(NFPlist_atk[i]) if len(NFPlist_atk[i]) > 0 else "N/A"
            mean_UV = np.mean(UVlist_atk[i]) if len(UVlist_atk[i]) > 0 else "N/A"
            std_UV = np.std(UVlist_atk[i]) if len(UVlist_atk[i]) > 0 else "N/A"
            
            # Write the data for the current number of obstacles with standard deviation
            outfile.write(f"{n_obs} | {mean_TFC} ({std_TFC}) | {mean_Cap} ({std_Cap}) | {mean_NFP} ({std_NFP}) | {mean_UV} ({std_UV})\n")
    
    print("Analysis summary has been written to AnalysisSummary.txt")









############################################################################################
'''
PlotAnalysis_IncreaseTrails_layrate() was used to generate the plot for Experiment 1 (figure 4) 
in the paper "Detection and Mitigation of Misleading Pheromone Trails in Foraging Robot Swarms"
'''
############################################################################################
def PlotAnalysis_IncreaseTrails_layrate():
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 24
    y_tick_fontsize = 24
    xlabel_fontsize = 32
    ylabel_fontsize = 32
    legend_fontsize = 24

    # Define lay rates and get all filenames in directory for attack only
    lay_rates = ["1", "4", "8", "12"]
    flist_attackData = []
    for filename in os.listdir("./results/analysis_layrate_MLT/results_analysis4_r24_1800_rc30it"):
        if filename.endswith("AttackData.txt"):
            flist_attackData.append(os.path.join("./results/analysis_layrate_MLT/results_analysis4_r24_1800_rc30it", filename))

    # Sort the filenames based on lay rates
    flist_attackData.sort(key=extract_rlp_value)  # Use an appropriate function to extract lay rate values

    # Parse data from files
    TFClist_atk = []
    Caplist_atk = []
    for filename in flist_attackData:
        Read2(filename)  # Ensure Read2 function processes the file correctly
        TFClist_atk.append(np.array(TOTAL_FOOD_COLLECTED).astype(int))
        Caplist_atk.append(np.array(ROBOTS_CAPTURED).astype(int))

    # Calculate percentages
    TFC_percent_atk = [(data / total_food) * 100 for data in TFClist_atk]
    Cap_percent_atk = [(data / total_robots) * 100 for data in Caplist_atk]

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

    # Calculate positions for boxplots
    gap = 0.5
    width = 0.35
    num_lay_rates = len(lay_rates)
    positions = np.arange(1, num_lay_rates * 2, step=2)

    # Plot boxplots and trend lines
    for i in range(num_lay_rates):
        box_pos = positions[i]
        axes[0].boxplot(TFC_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))
        axes[1].boxplot(Cap_percent_atk[i], positions=[box_pos], widths=width, patch_artist=True, boxprops=dict(facecolor="cyan"))

    # Plot trend lines
    trend_positions = np.array(positions) + width / 2
    axes[0].plot(trend_positions, [np.mean(data) for data in TFC_percent_atk], color="cyan", marker='o', label='Attack Only')
    axes[1].plot(trend_positions, [np.mean(data) for data in Cap_percent_atk], color="cyan", marker='o', label='Attack Only')

    # Axes labels and legends
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(lay_rates)
    axes[0].set_yticks(np.arange(20, 101, 20))
    axes[0].set_ylabel('Total Resources\nCollected (%)', fontsize=ylabel_fontsize, labelpad=15)
    axes[0].legend(fontsize=legend_fontsize)
    axes[1].set_xlabel(r"Rate of Laying Pheromone ($\lambda_{fg}$, $\lambda_{dt}$)", fontsize=xlabel_fontsize, labelpad=15)
    axes[1].set_ylabel('Total Foragers\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=15)

    # Uniform tick sizes and adjust layout
    for ax in axes:
        ax.tick_params(axis='x', labelsize=x_tick_fontsize)
        ax.tick_params(axis='y', labelsize=y_tick_fontsize)
    plt.tight_layout(pad=2.0)

    # Save the plot
    plt.savefig('./results/analysis_layrate_MLT/results_analysis4_r24_1800_rc30it/PlotAnalysis_IncreaseTrails.png')


############################################################################################
'''
PlotAnalysis_IncTrails_AtkDef() was used to generate the plot for Experiment 2-1 (figure 5) in 
the paper "Detection and Mitigation of Misleading Pheromone Trails in Foraging Robot Swarms"
'''
############################################################################################
def PlotAnalysis_IncTrails_AtkDef():
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 24
    y_tick_fontsize = 24
    xlabel_fontsize = 32
    ylabel_fontsize = 32
    legend_fontsize = 23

   # Calculate positions for boxplots# get all filenames in directory for attack only
    flist_atk = []
    for filename in os.listdir("./results/resultsExp8_LOG_PER_MIN_DATA_RateIncrease_r24_rlpf4.0_rlpd1.0_st1800_30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_atk.append(os.path.join("./results/resultsExp8_LOG_PER_MIN_DATA_RateIncrease_r24_rlpf4.0_rlpd1.0_st1800_30it", filename))
        else:
            continue

    # get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_atk.sort(key=extract_d_value)
    flist_atkdef.sort(key=extract_d_value)

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
    Cap_percent_atk = [(data / (total_robots)) * 100 for data in Caplist_atk] # 25% are detractors, so 75% are normal agents
    TFC_percent_atkdef = [(data / total_food) * 100 for data in TFClist_atkdef]
    Cap_percent_atkdef = [(data / (total_robots)) * 100 for data in Caplist_atkdef] # 25% are detractors, so 75% are normal agents

    # Detractor percentages
    detractor_percentages = ["0", "10", "20", "30", "40", "50"]
    det_perc = [0, 0.10, 0.20, 0.30, 0.40, 0.50]
    num_rates = len(detractor_percentages)

    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

    # Calculate positions for boxplots
    gap = 0.5  # Gap between each set of boxplots
    width = 0.2  # Boxplot width
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
    axes[0].set_xticklabels(detractor_percentages)
    axes[0].set_yticks(np.arange(25, 101, 15))
    axes[0].set_ylabel('Total Resources\nCollected (%)', fontsize=ylabel_fontsize, labelpad=13)
    axes[0].tick_params(axis='y', labelsize=y_tick_fontsize)
    axes[0].legend(fontsize=legend_fontsize, frameon=False)
    axes[1].set_xlabel('Percentage of Detractors (%)', fontsize=xlabel_fontsize, labelpad=20)
    axes[1].set_ylabel('Total Foragers\nCaptured (%)', fontsize=ylabel_fontsize, labelpad=9)
    axes[1].tick_params(axis='x', labelsize=x_tick_fontsize)
    axes[1].tick_params(axis='y', labelsize=y_tick_fontsize)
    # axes[1].legend()

    plt.tight_layout()
    plt.savefig('./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it/PlotAnalysis_IncreaseTrails_AtkDef.png')


############################################################################################
'''
plot_foragers_captured_per_min_moving_average_bar() was used to generate the plot for Experiment 2-2
(figure 6) in the paper "Detection and Mitigation of Misleading Pheromone Trails in Foraging Robot Swarms"
'''
############################################################################################
def plot_foragers_captured_per_min_moving_average_bar(directory_path, window_size=3):
    total_robots = 24
    total_food = 288

    x_tick_fontsize = 32
    y_tick_fontsize = 32
    xlabel_fontsize = 48
    ylabel_fontsize = 48
    title_fontsize = 40
    legend_fontsize = 32

    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    det_percentages = ["10%", "20%", "30%", "40%", "50%"]
    data_per_file = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]
            data_per_file.append(data)

    aggregated_data_per_file = []
    for data in data_per_file:
        aggregated_data = [data[i::30] for i in range(16)]  # Adjusted to 16 minutes
        aggregated_data_per_file.append(aggregated_data)

    fig, axes = plt.subplots(nrows=len(aggregated_data_per_file), ncols=1, figsize=(20, 6 * len(aggregated_data_per_file)), sharex=True)

    for i, aggregated_data in enumerate(aggregated_data_per_file):
        means = [np.mean(minute_data) for minute_data in aggregated_data]

        # Calculate moving average
        moving_averages = np.convolve(means, np.ones(window_size)/window_size, mode='valid')

        # Bar plot for actual data
        axes[i].bar(range(1, 17), means, color='cyan', alpha=0.5)

        # Plot moving average
        axes[i].plot(range(window_size, 17), moving_averages, color='blue', linewidth=2)

        # axes[i].set_ylabel('Foragers Captured', fontsize=ylabel_fontsize, labelpad=15)
        axes[i].tick_params(axis='y', labelsize=y_tick_fontsize)
        axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)
        
        # Format y-axis ticks to two decimal points
        axes[i].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        axes[i].set_yticks(np.arange(0.0,3.25,0.75))

        if i == 2:
            axes[i].set_ylabel('Foragers Captured', fontsize=ylabel_fontsize, labelpad=50)
        
        # Add legend only to the top subplot
        # if i == 4:
            # axes[i].legend([f'{window_size}-Minute Moving Average', 'Actual Data'], fontsize=legend_fontsize)

    axes[-1].set_xticks(range(1, 17))
    axes[-1].set_xlabel('Time (minutes)', fontsize=xlabel_fontsize, labelpad = 25)
    axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

    plt.tight_layout(pad=4.0)
    plt.savefig(os.path.join(directory_path, 'ForagersCapturedBarMovingAverage.png'))


def plot_foragers_captured_per_min_with_atkonly_overlay(directory_path1, directory_path2, window_size=3):
    total_robots = 24
    total_food = 288

    x_tick_fontsize = 32
    y_tick_fontsize = 32
    xlabel_fontsize = 48
    ylabel_fontsize = 48
    title_fontsize = 40
    legend_fontsize = 32

    file_paths1 = [os.path.join(directory_path1, f) for f in os.listdir(directory_path1) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths1.sort(key=extract_d_value)
    file_paths1 = [f for f in file_paths1 if "d0" not in f]

    file_paths2 = [os.path.join(directory_path2, f) for f in os.listdir(directory_path2) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths2.sort(key=extract_d_value)
    file_paths2 = [f for f in file_paths2 if "d0" not in f]

    det_percentages = ["10%", "20%", "30%", "40%", "50%"]

    fig, axes = plt.subplots(nrows=len(file_paths1), ncols=1, figsize=(20, 6 * len(file_paths1)), sharex=True)

    bar_width = 0.35  # Width of the bars
    index = np.arange(16)  # Time minutes from 1 to 16

    for i, (file_path1, file_path2) in enumerate(zip(file_paths1, file_paths2)):
        with open(file_path1, 'r') as file:
            next(file)  # Skip the header
            data1 = [float(line.strip()) for line in file.readlines()]
        
        with open(file_path2, 'r') as file:
            next(file)  # Skip the header
            data2 = [float(line.strip()) for line in file.readlines()]
        
        means1 = [np.mean(data1[j::30]) for j in range(16)]
        means2 = [np.mean(data2[j::30]) for j in range(16)]

        # Calculate moving averages for both sets
        moving_avg1 = np.convolve(means1, np.ones(window_size)/window_size, mode='valid')
        moving_avg2 = np.convolve(means2, np.ones(window_size)/window_size, mode='valid')

        # Valid indices for moving averages
        valid_indices = np.arange(window_size-1, 16)  # Adjust for valid range of moving average

        # Bar plot for defense data
        axes[i].bar(index - bar_width/2, means1, bar_width, color='cyan', alpha=0.5, label='With Defense' if i == 0 else "")

        # Bar plot for attack-only data
        axes[i].bar(index + bar_width/2, means2, bar_width, color='magenta', alpha=0.5, label='Attack Only' if i == 0 else "")

        # Line plot for moving averages
        axes[i].plot(valid_indices, moving_avg1, 'b-', linewidth=2)  # Removed label
        axes[i].plot(valid_indices, moving_avg2, 'r-', linewidth=2)  # Removed label

        axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)
        axes[i].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

        if i == 0:
            axes[i].legend(fontsize=legend_fontsize, loc='upper left')

        if i == len(file_paths1) // 2:
            axes[i].set_ylabel('Foragers Captured', fontsize=ylabel_fontsize, labelpad=50)

    axes[-1].set_xticks(index)
    axes[-1].set_xlabel('Time (minutes)', fontsize=xlabel_fontsize, labelpad = 25)
    axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

    plt.tight_layout(pad=4.0)
    plt.savefig(os.path.join(directory_path1, 'ForagersCapturedWithAtkOnlyOverlay.png'))

def output_foragers_captured_per_min_with_atkonly_overlay_to_file(directory_path1, directory_path2, output_file, window_size=3):
    file_paths1 = [os.path.join(directory_path1, f) for f in os.listdir(directory_path1) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths1.sort(key=extract_d_value)
    file_paths1 = [f for f in file_paths1 if "d0" not in f]

    file_paths2 = [os.path.join(directory_path2, f) for f in os.listdir(directory_path2) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths2.sort(key=extract_d_value)
    file_paths2 = [f for f in file_paths2 if "d0" not in f]

    with open(output_file, 'w') as f:
        f.write("Detractor Percentage,Minute,Mean (Defense),Mean (Attack Only),Moving Avg (Defense),Moving Avg (Attack Only)\n")
        
        for i, (file_path1, file_path2) in enumerate(zip(file_paths1, file_paths2)):
            with open(file_path1, 'r') as file:
                next(file)  # Skip the header
                data1 = [float(line.strip()) for line in file.readlines()]
            
            with open(file_path2, 'r') as file:
                next(file)  # Skip the header
                data2 = [float(line.strip()) for line in file.readlines()]
            
            means1 = [np.mean(data1[j::30]) for j in range(16)]
            means2 = [np.mean(data2[j::30]) for j in range(16)]

            moving_avg1 = np.convolve(means1, np.ones(window_size)/window_size, mode='valid')
            moving_avg2 = np.convolve(means2, np.ones(window_size)/window_size, mode='valid')

            valid_indices = np.arange(window_size-1, 16)  # Adjust for valid range of moving average

            for minute in range(16):
                f.write(f"{i*10+10}%,{minute+1},{means1[minute]:.2f},{means2[minute]:.2f},")
                if minute in valid_indices:
                    f.write(f"{moving_avg1[minute-window_size+1]:.2f},{moving_avg2[minute-window_size+1]:.2f}\n")
                else:
                    f.write(",,\n")



############################################################################################
'''
plot_detractors_isolated_per_min_moving_average_bar() was used to generate the plot for Experiment 2-3 
(figure 7) in the paper "Detection and Mitigation of Misleading Pheromone Trails in Foraging Robot Swarms"
'''
############################################################################################
def plot_detractors_isolated_per_min_moving_average_bar(directory_path, window_size=3):
    total_robots = 24
    total_food = 288

    x_tick_fontsize = 32
    y_tick_fontsize = 32
    xlabel_fontsize = 48
    ylabel_fontsize = 48
    title_fontsize = 40
    legend_fontsize = 32

    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("DetractorsIsolatedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    det_percentages = ["10%", "20%", "30%", "40%", "50%"]
    data_per_file = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]
            data_per_file.append(data)

    aggregated_data_per_file = []
    for data in data_per_file:
        aggregated_data = [data[i::30] for i in range(16)]  # Adjusted to 16 minutes
        aggregated_data_per_file.append(aggregated_data)

    fig, axes = plt.subplots(nrows=len(aggregated_data_per_file), ncols=1, figsize=(20, 6 * len(aggregated_data_per_file)), sharex=True)

    for i, aggregated_data in enumerate(aggregated_data_per_file):
        means = [np.mean(minute_data) for minute_data in aggregated_data]

        # Calculate moving average
        moving_averages = np.convolve(means, np.ones(window_size)/window_size, mode='valid')

        # Bar plot for actual data
        axes[i].bar(range(1, 17), means, color='cyan', alpha=0.5)

        # Plot moving average
        axes[i].plot(range(window_size, 17), moving_averages, color='blue', linewidth=2)

        # axes[i].set_ylabel('Detractors Isolated', fontsize=ylabel_fontsize, labelpad=15)
        axes[i].tick_params(axis='y', labelsize=y_tick_fontsize)
        axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)
        
        # Format y-axis ticks to two decimal points
        axes[i].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        axes[i].set_yticks(np.arange(0.0,0.8,0.2))

        if i == 2:
            axes[i].set_ylabel('Detractors Isolated', fontsize=ylabel_fontsize, labelpad=50)

        # Add legend only to the top subplot
        # if i == 4:
            # axes[i].legend([ f'{window_size}-Minute Moving Average','Actual Data'], fontsize=legend_fontsize)

    axes[-1].set_xticks(range(1, 17))
    axes[-1].set_xlabel('Time (minutes)', fontsize=xlabel_fontsize, labelpad = 25)
    axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

    plt.tight_layout(pad=4.0)
    plt.savefig(os.path.join(directory_path, 'DetractorsIsolatedBarMovingAverage.png'))










def plot_resources_per_min(directory_path):
    total_robots = 24
    total_food = 288

    # Font size variables
    x_tick_fontsize = 18
    y_tick_fontsize = 18
    xlabel_fontsize = 24
    ylabel_fontsize = 24
    title_fontsize = 24

    # Find all relevant files
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("ResourcePerMin.txt")]

    # Read data from files
    data_per_file = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]
            data_per_file.append(data)

    # Aggregate data for each minute across all simulations
    aggregated_data_per_file = []
    for data in data_per_file:
        aggregated_data = [data[i::30] for i in range(30)]  # Assuming 30 minutes per simulation
        aggregated_data_per_file.append(aggregated_data)

    # Number of minutes
    num_minutes = 30  # Assuming 30 minutes per simulation

    # Creating subplots
    fig, axes = plt.subplots(nrows=len(aggregated_data_per_file), ncols=1, figsize=(20, 6 * len(aggregated_data_per_file)), sharex=True)

    det_percentages = ["0%", "10%", "20%", "30%", "40%", "50%"]

    for i, aggregated_data in enumerate(aggregated_data_per_file):
        # Mean of each minute
        means = [np.mean(minute_data) for minute_data in aggregated_data]

        # Plot boxplot and mean line
        axes[i].boxplot(aggregated_data, positions=range(1, num_minutes + 1), widths=0.6, patch_artist=True)
        axes[i].plot(range(1, num_minutes + 1), means, color='red', marker='o', label='Mean per Minute')

        # Set labels and titles
        axes[i].set_title(f'Resources Collected Per Minute (File {i+1})')
        axes[i].set_ylabel('Resources Collected', fontsize=ylabel_fontsize)
        axes[i].tick_params(axis='y', labelsize=y_tick_fontsize)
        axes[i].legend()
        axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)

    # Set x-axis labels
    axes[-1].set_xticks(range(1, num_minutes + 1))
    axes[-1].set_xlabel('Simulated Minute', fontsize=xlabel_fontsize)
    axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

    # Adjust layout and save plot
    plt.tight_layout(pad=4.0)
    plt.savefig(os.path.join(directory_path, 'AggregatedResourcesPerMinutePlot.png'))

def plot_detractors_isolated_per_min(directory_path, window_size=3):
    total_robots = 24
    total_food = 288

    x_tick_fontsize = 24
    y_tick_fontsize = 24
    xlabel_fontsize = 32
    ylabel_fontsize = 32
    title_fontsize = 32

    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("DetractorsIsolatedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    det_percentages = ["10%", "20%", "30%", "40%", "50%"]
    data_per_file = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]
            data_per_file.append(data)

    aggregated_data_per_file = []
    for data in data_per_file:
        aggregated_data = [data[i::30] for i in range(16)]  # Adjusted to 16 minutes
        aggregated_data_per_file.append(aggregated_data)

    fig, axes = plt.subplots(nrows=len(aggregated_data_per_file), ncols=1, figsize=(20, 6 * len(aggregated_data_per_file)), sharex=True)

    for i, aggregated_data in enumerate(aggregated_data_per_file):
        means = [np.mean(minute_data) for minute_data in aggregated_data]

        # Calculate moving average
        moving_averages = np.convolve(means, np.ones(window_size)/window_size, mode='valid')

        axes[i].plot(range(1, 17), means, color='red', marker='o', label='Mean per Minute')
        axes[i].plot(range(window_size, 17), moving_averages, color='blue', label=f'{window_size}-Minute Moving Average')
        axes[i].set_ylabel('Detractors Isolated', fontsize=ylabel_fontsize, labelpad=15)
        axes[i].tick_params(axis='y', labelsize=y_tick_fontsize)
        axes[i].legend()
        axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)

    axes[-1].set_xticks(range(1, 17))
    axes[-1].set_xlabel('Simulated Minute', fontsize=xlabel_fontsize)
    axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

    plt.tight_layout(pad=4.0)
    plt.savefig(os.path.join(directory_path, 'DetractorsIsolatedPerMinuteWithMovingAverage.png'))

def plot_detractors_isolated_per_min_moving_average_only(directory_path, window_size=3):
    total_robots = 24
    total_food = 288

    x_tick_fontsize = 24
    y_tick_fontsize = 24
    xlabel_fontsize = 32
    ylabel_fontsize = 32
    title_fontsize = 32

    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("DetractorsIsolatedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    det_percentages = ["10%", "20%", "30%", "40%", "50%"]
    data_per_file = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]
            data_per_file.append(data)

    aggregated_data_per_file = []
    for data in data_per_file:
        aggregated_data = [data[i::30] for i in range(16)]  # Adjusted to 16 minutes
        aggregated_data_per_file.append(aggregated_data)

    fig, axes = plt.subplots(nrows=len(aggregated_data_per_file), ncols=1, figsize=(20, 6 * len(aggregated_data_per_file)), sharex=True)

    for i, aggregated_data in enumerate(aggregated_data_per_file):
        means = [np.mean(minute_data) for minute_data in aggregated_data]

        # Calculate moving average
        moving_averages = np.convolve(means, np.ones(window_size)/window_size, mode='valid')

        # Plot only moving average
        axes[i].plot(range(window_size, 17), moving_averages, color='blue', label=f'{window_size}-Minute Moving Average')
        axes[i].set_ylabel('Detractors Isolated', fontsize=ylabel_fontsize, labelpad=15)
        axes[i].tick_params(axis='y', labelsize=y_tick_fontsize)
        axes[i].legend()
        axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)

    axes[-1].set_xticks(range(1, 17))
    axes[-1].set_xlabel('Simulated Minute', fontsize=xlabel_fontsize)
    axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

    plt.tight_layout(pad=4.0)
    plt.savefig(os.path.join(directory_path, 'DetractorsIsolatedMovingAverageOnly.png'))

def output_foragers_cap_per_min(directory_path):
    # Similar setup as in your plotting function
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    # Detractor percentages
    det_percentages = ["10%", "20%", "30%", "40%", "50%"]

    # Process and output data
    for file_path, det_percentage in zip(file_paths, det_percentages):
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]

            # Aggregate data for each minute across all simulations
            aggregated_data = [data[i::30] for i in range(30)]  # Assuming 30 minutes per simulation

            # Output statistics for each minute
            print(f"Detractor Percentage: {det_percentage}")
            for minute, minute_data in enumerate(aggregated_data, start=1):
                mean = np.mean(minute_data)
                median = np.median(minute_data)
                min_val = min(minute_data)
                max_val = max(minute_data)
                std_dev = np.std(minute_data)

                print(f"Minute {minute}: Mean={mean}, Median={median}, Min={min_val}, Max={max_val}, StdDev={std_dev}")

def output_foragers_cap_per_min_to_file(directory_path, output_file):
    # Similar setup as in your plotting function
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("ForagersCapturedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    # Detractor percentages
    det_percentages = ["10%", "20%", "30%", "40%", "50%"]

    with open(output_file, 'w') as out_file:
        # Process and output data
        for file_path, det_percentage in zip(file_paths, det_percentages):
            with open(file_path, 'r') as file:
                next(file)  # Skip the header
                data = [float(line.strip()) for line in file.readlines()]

                # Aggregate data for each minute across all simulations
                aggregated_data = [data[i::30] for i in range(30)]  # Assuming 30 minutes per simulation

                # Output statistics for each minute
                out_file.write(f"Detractor Percentage: {det_percentage}\n")
                for minute, minute_data in enumerate(aggregated_data, start=1):
                    mean = np.mean(minute_data)
                    median = np.median(minute_data)
                    min_val = min(minute_data)
                    max_val = max(minute_data)
                    std_dev = np.std(minute_data)

                    out_file.write(f"Minute {minute}: Mean={mean}, Median={median}, Min={min_val}, Max={max_val}, StdDev={std_dev}\n")
                out_file.write("\n")

def output_detractors_iso_per_min(directory_path):
    # Font size variables
    title_fontsize = 32

    # Find all relevant files
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("DetractorsIsolatedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    # Detractor percentages
    det_percentages = ["10%", "20%", "30%", "40%", "50%"]

    # Process and output data
    for file_path, det_percentage in zip(file_paths, det_percentages):
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            data = [float(line.strip()) for line in file.readlines()]

            # Aggregate data for each minute across all simulations
            aggregated_data = [data[i::30] for i in range(30)]  # Assuming 30 minutes per simulation

            # Output statistics for each minute
            print(f"Detractor Percentage: {det_percentage} ({title_fontsize})")
            for minute, minute_data in enumerate(aggregated_data, start=1):
                mean = np.mean(minute_data)
                median = np.median(minute_data)
                min_val = min(minute_data)
                max_val = max(minute_data)
                std_dev = np.std(minute_data)

                print(f"Minute {minute}: Mean={mean}, Median={median}, Min={min_val}, Max={max_val}, StdDev={std_dev}")

def output_detractors_iso_per_min_to_file(directory_path, output_file):
    # Find all relevant files
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("DetractorsIsolatedPerMin.txt")]
    file_paths.sort(key=extract_d_value)
    file_paths = [f for f in file_paths if "d0" not in f]

    # Detractor percentages
    det_percentages = ["10%", "20%", "30%", "40%", "50%"]

    with open(output_file, 'w') as out_file:
        # Process and output data
        for file_path, det_percentage in zip(file_paths, det_percentages):
            with open(file_path, 'r') as file:
                next(file)  # Skip the header
                data = [float(line.strip()) for line in file.readlines()]

                # Aggregate data for each minute across all simulations
                aggregated_data = [data[i::30] for i in range(30)]  # Assuming 30 minutes per simulation

                # Output statistics for each minute
                out_file.write(f"Detractor Percentage: {det_percentage}\n")
                for minute, minute_data in enumerate(aggregated_data, start=1):
                    mean = np.mean(minute_data)
                    median = np.median(minute_data)
                    min_val = min(minute_data)
                    max_val = max(minute_data)
                    std_dev = np.std(minute_data)

                    out_file.write(f"Minute {minute}: Mean={mean}, Median={median}, Min={min_val}, Max={max_val}, StdDev={std_dev}\n")
                out_file.write("\n")

def output_atkdef(directory_path_atk, directory_path_atkdef):
    total_robots = 24
    total_food = 288

    # Function to read data from a file
    def read_data(file_path):
        with open(file_path, 'r') as file:
            return [int(line.strip()) for line in file]

    # Get all filenames
    flist_atk = [os.path.join(directory_path_atk, f) for f in os.listdir(directory_path_atk) if f.endswith("AttackData.txt")]
    flist_atkdef = [os.path.join(directory_path_atkdef, f) for f in os.listdir(directory_path_atkdef) if f.endswith("AttackData.txt")]

    # Sort the filenames
    flist_atk.sort(key=extract_d_value)
    flist_atkdef.sort(key=extract_d_value)

    # Read and process data
    for file_atk, file_atkdef in zip(flist_atk, flist_atkdef):
        TFC_atk = read_data(file_atk)
        TFC_atkdef = read_data(file_atkdef)
        
        # Calculate percentages
        TFC_percent_atk = [(data / total_food) * 100 for data in TFC_atk]
        TFC_percent_atkdef = [(data / total_food) * 100 for data in TFC_atkdef]

        # Output statistics
        print(f"File: {os.path.basename(file_atk)}")
        print("Attack Only:")
        print(f"  Mean: {np.mean(TFC_percent_atk)}%")
        print(f"  Median: {np.median(TFC_percent_atk)}%")
        print(f"  Min: {np.min(TFC_percent_atk)}%")
        print(f"  Max: {np.max(TFC_percent_atk)}%")
        print(f"  StdDev: {np.std(TFC_percent_atk)}%")
        print("Attack with Defense:")
        print(f"  Mean: {np.mean(TFC_percent_atkdef)}%")
        print(f"  Median: {np.median(TFC_percent_atkdef)}%")
        print(f"  Min: {np.min(TFC_percent_atkdef)}%")
        print(f"  Max: {np.max(TFC_percent_atkdef)}%")
        print(f"  StdDev: {np.std(TFC_percent_atkdef)}%")
        print("-------------------------------------------")

def output_atkdef_to_file(output_file):
    total_robots = 24
    total_food = 288

   # Calculate positions for boxplots# get all filenames in directory for attack only
    flist_atk = []
    for filename in os.listdir("./results/resultsExp8_LOG_PER_MIN_DATA_RateIncrease_r24_rlpf4.0_rlpd1.0_st1800_30it"):
        if filename.endswith("AttackData.txt"):
            # print(filename)
            flist_atk.append(os.path.join("./results/resultsExp8_LOG_PER_MIN_DATA_RateIncrease_r24_rlpf4.0_rlpd1.0_st1800_30it", filename))
        else:
            continue

    # get all filenames in directory for attack with defense
    flist_atkdef = []
    for filename in os.listdir("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it"):
        if filename.endswith("AttackData.txt"):
            flist_atkdef.append(os.path.join("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it", filename))
        else:
            continue

    # Sort the filenames based on the extracted rlp value
    flist_atk.sort(key=extract_d_value)
    flist_atkdef.sort(key=extract_d_value)

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
    Cap_percent_atk = [(data / (total_robots)) * 100 for data in Caplist_atk] # 25% are detractors, so 75% are normal agents
    TFC_percent_atkdef = [(data / total_food) * 100 for data in TFClist_atkdef]
    Cap_percent_atkdef = [(data / (total_robots)) * 100 for data in Caplist_atkdef] # 25% are detractors, so 75% are normal agents


    with open(output_file, 'w') as out_file:
        # Read and process data
        for (file_atk, file_atkdef, TFC_atk, TFC_atkdef, Cap_atk, Cap_atkdef) in zip(flist_atk, flist_atkdef, TFClist_atk, TFClist_atkdef, Caplist_atk, Caplist_atkdef):
            # Calculate percentages for Total Food Collected and Robots Captured
            TFC_percent_atk = [(data / total_food) * 100 for data in TFC_atk]
            TFC_percent_atkdef = [(data / total_food) * 100 for data in TFC_atkdef]
            Cap_percent_atk = [(data / total_robots) * 100 for data in Cap_atk]
            Cap_percent_atkdef = [(data / total_robots) * 100 for data in Cap_atkdef]

            # Output statistics
            out_file.write(f"File: {os.path.basename(file_atk)}\n")
            out_file.write("Attack Only:\n")
            out_file.write(f"  Total Food Collected: Mean={np.mean(TFC_percent_atk)}%, Median={np.median(TFC_percent_atk)}%, Min={np.min(TFC_percent_atk)}%, Max={np.max(TFC_percent_atk)}%, StdDev={np.std(TFC_percent_atk)}%\n")
            out_file.write(f"  Robots Captured: Mean={np.mean(Cap_percent_atk)}%, Median={np.median(Cap_percent_atk)}%, Min={np.min(Cap_percent_atk)}%, Max={np.max(Cap_percent_atk)}%, StdDev={np.std(Cap_percent_atk)}%\n")
            out_file.write("Attack with Defense:\n")
            out_file.write(f"  Total Food Collected: Mean={np.mean(TFC_percent_atkdef)}%, Median={np.median(TFC_percent_atkdef)}%, Min={np.min(TFC_percent_atkdef)}%, Max={np.max(TFC_percent_atkdef)}%, StdDev={np.std(TFC_percent_atkdef)}%\n")
            out_file.write(f"  Robots Captured: Mean={np.mean(Cap_percent_atkdef)}%, Median={np.median(Cap_percent_atkdef)}%, Min={np.min(Cap_percent_atkdef)}%, Max={np.max(Cap_percent_atkdef)}%, StdDev={np.std(Cap_percent_atkdef)}%\n")
            out_file.write("-------------------------------------------\n")




# def plot_detractors_isolated_per_min(directory_path):
#     total_robots = 24
#     total_food = 288

#     # Font size variables
#     x_tick_fontsize = 18
#     y_tick_fontsize = 18
#     xlabel_fontsize = 24
#     ylabel_fontsize = 24
#     title_fontsize = 24

#     # Find all relevant files
#     file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith("DetractorsIsolatedPerMin.txt")]

#     # Sort files
#     file_paths.sort(key=extract_d_value)

#     # Read data from files
#     data_per_file = []
#     for file_path in file_paths:
#         with open(file_path, 'r') as file:
#             next(file)  # Skip the header
#             data = [float(line.strip()) for line in file.readlines()]
#             data_per_file.append(data)

#     # Aggregate data for each minute across all simulations
#     aggregated_data_per_file = []
#     for data in data_per_file:
#         aggregated_data = [data[i::30] for i in range(30)]  # Assuming 30 minutes per simulation
#         aggregated_data_per_file.append(aggregated_data)

#     # Number of minutes
#     num_minutes = 30  # Assuming 30 minutes per simulation

#     # Creating subplots
#     fig, axes = plt.subplots(nrows=len(aggregated_data_per_file), ncols=1, figsize=(20, 6 * len(aggregated_data_per_file)), sharex=True)

#     det_percentages = ["0%", "10%", "20%", "30%", "40%", "50%"]

#     for i, aggregated_data in enumerate(aggregated_data_per_file):
#         # Mean of each minute
#         means = [np.mean(minute_data) for minute_data in aggregated_data]

#         # Plot boxplot and mean line
#         axes[i].boxplot(aggregated_data, positions=range(1, num_minutes + 1), widths=0.6, patch_artist=True)
#         axes[i].plot(range(1, num_minutes + 1), means, color='red', marker='o', label='Mean per Minute')

#         # Set labels and titles
#         axes[i].set_ylabel('Detractors Isolated', fontsize=ylabel_fontsize, labelpad=15)
#         axes[i].tick_params(axis='y', labelsize=y_tick_fontsize)
#         axes[i].legend()
#         axes[i].set_title(f'Detractor Percentage: {det_percentages[i]}', fontsize=title_fontsize)

#     # Set x-axis labels
#     axes[-1].set_xticks(range(1, num_minutes + 1))
#     axes[-1].set_xlabel('Simulated Minute', fontsize=xlabel_fontsize)
#     axes[-1].tick_params(axis='x', labelsize=x_tick_fontsize)

#     # Adjust layout and save plot
#     plt.tight_layout(pad=4.0)
#     plt.savefig(os.path.join(directory_path, 'AggregatedDetractorsIsolatedPerMinutePlot.png'))











def print_data_summary(ratio_data, lay_rates):
    for i, lay_rate_data in enumerate(ratio_data):
        print(f"Lay Rate {lay_rates[i]}:")
        for j, sim_data in enumerate(lay_rate_data):
            if sim_data:
                min_val = min(sim_data)
                max_val = max(sim_data)
                avg_val = sum(sim_data) / len(sim_data)
                print(f"  Simulation {j + 1}: Min = {min_val}, Max = {max_val}, Avg = {avg_val}")
            else:
                print(f"  Simulation {j + 1}: No Data")

def extract_rlp_value(filename):
    """
    Extract the rlp value from the filename.
    Assumes the filename contains 'rlp' followed by a number (e.g., 'rlp8.0').
    """
    match = re.search(r"rlpf(\d+\.\d+)", filename)
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

def extract_ncobs_value(filename):
    """
    Extracts the 'ncobs' value from the filename.

    Args:
    filename (str): The filename from which to extract the 'ncobs' value.

    Returns:
    float: The extracted 'ncobs' value.
    """
    match = re.search(r"_ncobs(\d+)", filename)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("No 'ncobs' value found in filename.")

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
    # PlotExp_AtkDef_varyDetractorPercentage()
    # PlotExp_DefOnly_varyDetractorPercentage()
    # PlotExp_DefOnly_performanceEval()

    # PlotAnalysis1_st1800()
    # PlotAnalysis1_st2700()
    # PlotAnalysis1_NotLetDetractorsUseMLT()
    # PlotAnalysis2_NotLetDetractorsUseMLT()
    # PlotAnalysis3()
    # PlotAnalysis4()
    # PlotAnalysis_IncreaseTrails()
    # PlotAnalysis_IncTrails_AtkDef()
    
    # plot_resources_per_min("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it")
    # plot_foragers_captured_per_min("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it")
    # plot_detractors_isolated_per_min("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it")
    # plot_detractors_isolated_per_min_moving_average_only("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it")

    # plot_detractors_isolated_per_min_moving_average_bar("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it")
    # plot_foragers_captured_per_min_moving_average_bar("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it")

    # plot_foragers_captured_per_min_with_atkonly_overlay("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it", 
    #                                                     "./results/resultsExp10-2_atkonly_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_20it", 
    #                                                     window_size=3)

    output_foragers_captured_per_min_with_atkonly_overlay_to_file("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it", 
                                                        "./results/resultsExp10-2_atkonly_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_20it",
                                                        "./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it/ForagersCapturedPerMinWithAtkOverlayResults.txt", 
                                                        window_size=3)
    # PlotAnalysis_IncreaseTrails_layrate()
    # Output_IncreaseTrails_layrate("./results/analysis_layrate_MLT/results_analysis4_r24_1800_rc30it/layrate_results.txt")

    # PlotAnalysis_VaryNumCylinderObstacles_AtkDef()

    # output_foragers_cap_per_min_to_file("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it", "./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it/ForagersCapturedPerMinResults.txt")
    # output_detractors_iso_per_min_to_file("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it", "./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it/DetractorsIsolatedPerMinResults.txt")
    # output_atkdef_to_file("./results/resultsExp10_LOG_PER_MIN_DATA_RateIncrease_DEF_PRI_r24_rlpf4_rlpd1_st1800_30it/AttackWithDefenseResults.txt")
