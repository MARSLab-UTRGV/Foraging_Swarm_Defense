import DoS_xml_config as config
import os, time
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import shutil, sys
np.set_printoptions(suppress=True)

SIM_TIME = []
TOTAL_FOOD_COLLECTED = []
TOTAL_COLLECTION_RATE = []
REAL_FOOD_COLLECTED = []
REAL_COLLECTION_RATE = []
FAKE_FOOD_COLLECTED = []
FAKE_COLLECTION_RATE = []
REAL_PTRAILS_CREATED = []
FAKE_PTRAILS_CREATED = []

def Read(fname):
    count = 0
    SIM_TIME.clear()
    TOTAL_FOOD_COLLECTED.clear()
    TOTAL_COLLECTION_RATE.clear()
    REAL_FOOD_COLLECTED.clear()
    REAL_COLLECTION_RATE.clear()
    FAKE_FOOD_COLLECTED.clear()
    FAKE_COLLECTION_RATE.clear()
    REAL_PTRAILS_CREATED.clear()
    FAKE_PTRAILS_CREATED.clear()
    
    with open(fname) as f:
        for line in f.readlines():
            data = line.strip().split(',')
            if data[0] == 'Simulation Time (seconds)':
                continue
            SIM_TIME.append(data[0])
            TOTAL_FOOD_COLLECTED.append(data[1])
            TOTAL_COLLECTION_RATE.append(data[2])
            REAL_FOOD_COLLECTED.append(data[3])
            REAL_COLLECTION_RATE.append(data[4])
            FAKE_FOOD_COLLECTED.append(data[5])
            FAKE_COLLECTION_RATE.append(data[6])
            REAL_PTRAILS_CREATED.append(data[7])
            FAKE_PTRAILS_CREATED.append(data[8])

def PlotExp1(flist, maxRealFood, maxFakeFood):

    RFClist = []
    FFClist = []
    for filename in flist:
        Read(filename)
        RFClist.append(np.array(REAL_FOOD_COLLECTED).astype(float))
        FFClist.append(np.array(FAKE_FOOD_COLLECTED).astype(float))
    
    RFCdata = []
    for r in RFClist:
        RFCdata.append((round(np.mean(r),1),np.std(r)))
    FFCdata = []
    for f in FFClist:
        FFCdata.append((round(np.mean(f),1),np.std(f)))

    num_clusters = ['1','2','3','4','5']

    data = [
        ('CPFA\n(Standard)',            (RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0]),    # Real Food Collected Means
                                        (RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1]),    # Real Food Collected StdDeviation
                                        (FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0]),    # Fake Food Collected Means
                                        (FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1])),   # Fake Food Collected StdDeviation

        ('CPFA\n(+ Fake Resources)',    (RFCdata[1][0],RFCdata[4][0],RFCdata[7][0],RFCdata[10][0],RFCdata[13][0]),
                                        (RFCdata[1][1],RFCdata[4][1],RFCdata[7][1],RFCdata[10][1],RFCdata[13][1]),
                                        (FFCdata[1][0],FFCdata[4][0],FFCdata[7][0],FFCdata[10][0],FFCdata[13][0]),
                                        (FFCdata[1][1],FFCdata[4][1],FFCdata[7][1],FFCdata[10][1],FFCdata[13][1])),

        ('CPFA\n(+ QZones)',            (RFCdata[3][0],RFCdata[6][0],RFCdata[9][0],RFCdata[12][0],RFCdata[15][0]),
                                        (RFCdata[3][1],RFCdata[6][1],RFCdata[9][1],RFCdata[12][1],RFCdata[15][1]),
                                        (FFCdata[3][0],FFCdata[6][0],FFCdata[9][0],FFCdata[12][0],FFCdata[15][0]),
                                        (FFCdata[3][1],FFCdata[6][1],FFCdata[9][1],FFCdata[12][1],FFCdata[15][1]))
    ]

    x = np.arange(len(num_clusters))
    width=0.3
    multiplier=0

    fig,ax=plt.subplots(figsize=(10,8),nrows=2, sharex=True)
    labelsize = 9

    offset = width * multiplier
    rect1 = ax[0].bar(x+offset, data[0][1], width, align="center", yerr=data[0][2], ecolor='orange', label=data[0][0], edgecolor='black', color='blue', zorder=10)
    rect2 = ax[1].bar(x+offset, data[0][3], width, align="center", yerr=data[0][4], ecolor='orange', label=data[0][0], edgecolor='black', hatch='xx', color='blue', zorder=10)
    ax[0].bar_label(rect1,padding=10, fontsize=labelsize)
    multiplier+=1

    offset = width * multiplier
    rect3 = ax[0].bar(x+offset, data[1][1], width, align="center", yerr=data[1][2], ecolor='orange', label=data[1][0], edgecolor='black', color='green', zorder=10)
    rect4 = ax[1].bar(x+offset, data[1][3], width, align="center", yerr=data[1][4], ecolor='orange', label=data[1][0], edgecolor='black', hatch='xx', color='green', zorder=10)
    ax[0].bar_label(rect3,padding=10, fontsize=labelsize)
    ax[1].bar_label(rect4,padding=-15, fontsize=labelsize)
    multiplier+=1

    offset = width * multiplier
    rect5 = ax[0].bar(x+offset, data[2][1], width, align="center", yerr=data[2][2], ecolor='orange', label=data[2][0], edgecolor='black', color='red', zorder=10)
    rect6 = ax[1].bar(x+offset, data[2][3], width, align="center", yerr=data[2][4], ecolor='orange', label=data[2][0], edgecolor='black', hatch='xx', color='red', zorder=10)
    ax[0].bar_label(rect5,padding=10, fontsize=labelsize)
    ax[1].bar_label(rect6,padding=-15, fontsize=labelsize)
    multiplier+=1

    
    fig.legend(loc='lower center', bbox_to_anchor=(0.525,0.1), ncols=2)

    ax[0].set_ylim(0,maxRealFood)
    ax[0].set_ylabel('Real Resources Collected')
    ax[1].set_ylim(0,maxFakeFood)
    ax[1].set_ylabel('Fake Resources Collected')
    ax[1].invert_yaxis()

    ax[1].set_xticks(x+width, num_clusters)
    ax[1].xaxis.tick_bottom()
    ax[1].set_xlabel('Number of Fake Resource Clusters (6x6)')

    ax[0].set_title('Foraging Results by Number of Fake Resource Clusters')

    fig.tight_layout()
    fig.subplots_adjust(hspace=0)

    plt.savefig('results/Experiment_1-classic.png')

def PlotExp1_v2(flist, rdpath, maxRealFood, maxFakeFood):

    RFClist = []
    FFClist = []

    for filename in flist:
        Read(filename)
        RFClist.append(np.array(REAL_FOOD_COLLECTED).astype(float))
        FFClist.append(np.array(FAKE_FOOD_COLLECTED).astype(float))
    
    RFCdata = []
    for r in RFClist:
        RFCdata.append((round(np.mean(r),1),np.std(r)))
    FFCdata = []
    for f in FFClist:
        FFCdata.append((round(np.mean(f),1),np.std(f)))

    x_tick_labels = ['1','2','3','4','5']


    data1 = [
        ('$FA_{R}$',                    (RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0],RFCdata[0][0]),    # Real Food Collected Means
                                        (RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1],RFCdata[0][1]),    # Real Food Collected StdDeviation
                                        (FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0],FFCdata[0][0]),    # Fake Food Collected Means
                                        (FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1],FFCdata[0][1])),   # Fake Food Collected StdDeviation

        ('$FA_{RF}$',                   (RFCdata[1][0],RFCdata[4][0],RFCdata[7][0],RFCdata[10][0],RFCdata[13][0]),
                                        (RFCdata[1][1],RFCdata[4][1],RFCdata[7][1],RFCdata[10][1],RFCdata[13][1]),
                                        (FFCdata[1][0],FFCdata[4][0],FFCdata[7][0],FFCdata[10][0],FFCdata[13][0]),
                                        (FFCdata[1][1],FFCdata[4][1],FFCdata[7][1],FFCdata[10][1],FFCdata[13][1])),

        ('$FA_{QZ}$',                   (RFCdata[2][0],RFCdata[5][0],RFCdata[8][0],RFCdata[11][0],RFCdata[14][0]),
                                        (RFCdata[2][1],RFCdata[5][1],RFCdata[8][1],RFCdata[11][1],RFCdata[14][1]),
                                        (FFCdata[2][0],FFCdata[5][0],FFCdata[8][0],FFCdata[11][0],FFCdata[14][0]),
                                        (FFCdata[2][1],FFCdata[5][1],FFCdata[8][1],FFCdata[11][1],FFCdata[14][1])),

        ('$FA_{QZ\_M}$',                (RFCdata[3][0],RFCdata[6][0],RFCdata[9][0],RFCdata[12][0],RFCdata[15][0]),
                                        (RFCdata[3][1],RFCdata[6][1],RFCdata[9][1],RFCdata[12][1],RFCdata[15][1]),
                                        (FFCdata[3][0],FFCdata[6][0],FFCdata[9][0],FFCdata[12][0],FFCdata[15][0]),
                                        (FFCdata[3][1],FFCdata[6][1],FFCdata[9][1],FFCdata[12][1],FFCdata[15][1]))
    ]

    x = np.arange(len(x_tick_labels))
    width=0.23
    multiplier=0

    fig,ax=plt.subplots(figsize=(14,10),nrows=2, sharex=True)
    labelsize = 14
    textsize = 23
    top_plt_pad = -125
    bottom_plt_pad = -25
    top_labelcolor = 'white'
    bottom_labelcolor = 'black'
    bar_zorder = 0
    label_zorder = 15
    b_label_rotation = 30

    offset = width * multiplier
    rect1 = ax[0].bar(x+offset, data1[0][1], width, align="center", yerr=data1[0][2], ecolor='orange', label=data1[0][0], edgecolor='black', color='blue', zorder=bar_zorder)
    ax[0].bar_label(rect1,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect3 = ax[0].bar(x+offset, data1[1][1], width, align="center", yerr=data1[1][2], ecolor='orange', label=data1[1][0], edgecolor='black', color='green', zorder=bar_zorder)
    rect4 = ax[1].bar(x+offset, data1[1][3], width, align="center", yerr=data1[1][4], ecolor='orange', label=data1[1][0], edgecolor='black', hatch='xx', color='green', zorder=bar_zorder)
    ax[0].bar_label(rect3,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    ax[1].bar_label(rect4,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect5 = ax[0].bar(x+offset, data1[2][1], width, align="center", yerr=data1[2][2], ecolor='orange', label=data1[2][0], edgecolor='black', color='red', zorder=bar_zorder)
    rect6 = ax[1].bar(x+offset, data1[2][3], width, align="center", yerr=data1[2][4], ecolor='orange', label=data1[2][0], edgecolor='black', hatch='xx', color='red', zorder=bar_zorder)
    ax[0].bar_label(rect5,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    ax[1].bar_label(rect6,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect7 = ax[0].bar(x+offset, data1[3][1], width, align="center", yerr=data1[3][2], ecolor='orange', label=data1[3][0], edgecolor='black', color='purple', zorder=bar_zorder)
    rect8 = ax[1].bar(x+offset, data1[3][3], width, align="center", yerr=data1[3][4], ecolor='orange', label=data1[3][0], edgecolor='black', hatch='xx', color='purple', zorder=bar_zorder)
    ax[0].bar_label(rect7,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    ax[1].bar_label(rect8,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1
    
    # ax[0].legend(loc='lower left', ncols=2, fontsize=textsize, bbox_to_anchor=(0, -0.1), zorder = 20)

    # First get the handles and labels from the axes
    handles1, labels1 = ax[0].get_legend_handles_labels()
    plt.legend(handles1, labels1, loc='lower left', ncol=2, fontsize=textsize)

    # ax[0].set_ylim(0,maxRealFood)
    ax[0].set_ylabel('Real Resources Collected', fontsize=textsize)
    ax[1].set_ylim(0,65)
    ax[1].set_ylabel('Fake Resources Collected', fontsize=textsize)
    ax[1].invert_yaxis()

    ax[1].set_xticks(x+width, x_tick_labels, fontsize=labelsize)
    ax[1].xaxis.tick_bottom()
    ax[1].set_xlabel('Number of Fake Food Clusters (6x6)', fontsize=textsize)

    # ax[0].set_title('Foraging Results by Maximum Simulation Time')

    fig.tight_layout()
    fig.subplots_adjust(hspace=0)

    plt.savefig(f'{rdpath}Experiment_1.png')

def PlotExp2_v1(flist, maxRealFood, maxFakeFood):

    RFClist = []
    FFClist = []
    for filename in flist:
        Read(filename)
        RFClist.append(np.array(REAL_FOOD_COLLECTED).astype(float))
        FFClist.append(np.array(FAKE_FOOD_COLLECTED).astype(float))
    
    RFCdata = []
    for r in RFClist:
        RFCdata.append((round(np.mean(r),1),np.std(r)))
        print(f'{round(np.mean(r),1)} +- {np.std(r)}')
    FFCdata = []
    for f in FFClist:
        FFCdata.append((round(np.mean(f),1),np.std(f)))
        print(f'{round(np.mean(f),1)} +- {np.std(f)}')

    x_tick_labels = ['10','15','20','25','30']

    # generate unicode subscript of letter F
    F = ['\u0394','\u0393','\u0388','\u0387','\u0386']

    data = [
        ('$FA_{R}$',                    (RFCdata[0][0],RFCdata[4][0],RFCdata[8][0],RFCdata[12][0],RFCdata[16][0]),    # Real Food Collected Means
                                        (RFCdata[0][1],RFCdata[4][1],RFCdata[8][1],RFCdata[12][1],RFCdata[16][1]),    # Real Food Collected StdDeviation
                                        (FFCdata[0][0],FFCdata[4][0],FFCdata[8][0],FFCdata[12][0],FFCdata[16][0]),    # Fake Food Collected Means
                                        (FFCdata[0][1],FFCdata[4][1],FFCdata[8][1],FFCdata[12][1],FFCdata[16][1])),   # Fake Food Collected StdDeviation

        ('$FA_{RF}$',                   (RFCdata[1][0],RFCdata[5][0],RFCdata[9][0],RFCdata[13][0],RFCdata[17][0]),
                                        (RFCdata[1][1],RFCdata[5][1],RFCdata[9][1],RFCdata[13][1],RFCdata[17][1]),
                                        (FFCdata[1][0],FFCdata[5][0],FFCdata[9][0],FFCdata[13][0],FFCdata[17][0]),
                                        (FFCdata[1][1],FFCdata[5][1],FFCdata[9][1],FFCdata[13][1],FFCdata[17][1])),

        ('$FA_{QZ}$',                   (RFCdata[2][0],RFCdata[6][0],RFCdata[10][0],RFCdata[14][0],RFCdata[18][0]),
                                        (RFCdata[2][1],RFCdata[6][1],RFCdata[10][1],RFCdata[14][1],RFCdata[18][1]),
                                        (FFCdata[2][0],FFCdata[6][0],FFCdata[10][0],FFCdata[14][0],FFCdata[18][0]),
                                        (FFCdata[2][1],FFCdata[6][1],FFCdata[10][1],FFCdata[14][1],FFCdata[18][1])),

        ('$FA_{QZ\_M}$',                (RFCdata[3][0],RFCdata[7][0],RFCdata[11][0],RFCdata[15][0],RFCdata[19][0]),
                                        (RFCdata[3][1],RFCdata[7][1],RFCdata[11][1],RFCdata[15][1],RFCdata[19][1]),
                                        (FFCdata[3][0],FFCdata[7][0],FFCdata[11][0],FFCdata[15][0],FFCdata[19][0]),
                                        (FFCdata[3][1],FFCdata[7][1],FFCdata[11][1],FFCdata[15][1],FFCdata[19][1]))
    ]

    x = np.arange(len(x_tick_labels))
    width=0.23
    multiplier=0

    fig,ax=plt.subplots(figsize=(14,10),nrows=2, sharex=True)
    labelsize = 14
    textsize = 23
    top_plt_pad = -125
    bottom_plt_pad = -25
    top_labelcolor = 'white'
    bottom_labelcolor = 'black'
    bar_zorder = 0
    label_zorder = 15
    b_label_rotation = 30

    offset = width * multiplier
    rect1 = ax[0].bar(x+offset, data[0][1], width, align="center", yerr=data[0][2], ecolor='orange', label=data[0][0], edgecolor='black', color='blue', zorder=bar_zorder)
    ax[0].bar_label(rect1,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect3 = ax[0].bar(x+offset, data[1][1], width, align="center", yerr=data[1][2], ecolor='orange', label=data[1][0], edgecolor='black', color='green', zorder=bar_zorder)
    rect4 = ax[1].bar(x+offset, data[1][3], width, align="center", yerr=data[1][4], ecolor='orange', label=data[1][0], edgecolor='black', hatch='xx', color='green', zorder=bar_zorder)
    ax[0].bar_label(rect3,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    ax[1].bar_label(rect4,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect5 = ax[0].bar(x+offset, data[2][1], width, align="center", yerr=data[2][2], ecolor='orange', label=data[2][0], edgecolor='black', color='red', zorder=bar_zorder)
    rect6 = ax[1].bar(x+offset, data[2][3], width, align="center", yerr=data[2][4], ecolor='orange', label=data[2][0], edgecolor='black', hatch='xx', color='red', zorder=bar_zorder)
    ax[0].bar_label(rect5,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    ax[1].bar_label(rect6,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1

    offset = width * multiplier
    rect7 = ax[0].bar(x+offset, data[3][1], width, align="center", yerr=data[3][2], ecolor='orange', label=data[3][0], edgecolor='black', color='purple', zorder=bar_zorder)
    rect8 = ax[1].bar(x+offset, data[3][3], width, align="center", yerr=data[3][4], ecolor='orange', label=data[3][0], edgecolor='black', hatch='xx', color='purple', zorder=bar_zorder)
    ax[0].bar_label(rect7,padding=top_plt_pad, fontsize=labelsize, color=top_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    ax[1].bar_label(rect8,padding=bottom_plt_pad, fontsize=labelsize, color=bottom_labelcolor, zorder=label_zorder, fontweight='bold', rotation=b_label_rotation)
    multiplier+=1
    
    # ax[0].legend(loc='lower left', ncols=2, fontsize=textsize, bbox_to_anchor=(0, -0.1), zorder = 20)

    # First get the handles and labels from the axes
    handles1, labels1 = ax[0].get_legend_handles_labels()
    plt.legend(handles1, labels1, loc='lower left', ncol=2, fontsize=textsize)

    # ax[0].set_ylim(0,maxRealFood)
    ax[0].set_ylabel('Real Resources Collected', fontsize=textsize)
    ax[1].set_ylim(0,85)
    ax[1].set_ylabel('Fake Resources Collected', fontsize=textsize, labelpad = 11)
    ax[1].invert_yaxis()

    ax[1].set_xticks(x+width, x_tick_labels, fontsize=labelsize)
    ax[1].xaxis.tick_bottom()
    ax[1].set_xlabel('Max Simulation Time (minutes)', fontsize=textsize)

    # ax[0].set_title('Foraging Results by Maximum Simulation Time')

    fig.tight_layout()
    fig.subplots_adjust(hspace=0)

    # plt.savefig('results/Experiment_2.png')
    plt.savefig('results_Exp2/Experiment_2.png')

def PlotPheromoneExperiment_v1(flist, maxFakeFood):
    
    FPlist = []
    for filename in flist:
        Read(filename)
        FPlist.append(np.array(FAKE_PTRAILS_CREATED).astype(float))
    
    FPdata = []
    for f in FPlist:
        FPdata.append((round(np.mean(f),1),np.std(f)))
        print(f'{round(np.mean(f),1)} +- {np.std(f)}')

    x_tick_labels = ['Standard', 'High']

    data = [
        (FPdata[0][0], FPdata[0][1]),
        (FPdata[1][0], FPdata[1][1]),
    ]

    # generate a boxplot using FPlist
    bp1 = plt.boxplot(FPlist, vert=1)
    ax = plt.gca()
    ax.set_ylabel('Number of Pheromone Trails Created')
    plt.xticks([1,2], x_tick_labels)
    plt.ylim(0,maxFakeFood)
    plt.savefig("PheromoneExperiment1_boxplot.png")
    plt.close()

def InitialExperiment():
    run_count = 50

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1000

    # Random Distribution Settings
    XML.NUM_RF = 128
    num_ff = [64,96,128,160,192]
    XML.NUM_FF = 128
    # Cluster Distribution Settings
    XML.NUM_RCL = 2
    num_fcl = [(1,8,8),(2,8,8), (3,8,8)]
    XML.NUM_FCL = 2
    # Powerlaw Distribution Settings
    XML.NUM_PLAW_RF = 128
    num_plaw_ff = [64,96,128,160,192]
    XML.NUM_PLAW_FF = 128

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods
        XML.setDistribution(i)
        print(f'Main Experiment, {run_count} iterations without Fake Food, {run_count} with Fake Food.\n')
        dmode = ""
        if i == 0:
            dmode = "Random"
            # Random
            for j in num_ff:
            
                XML.NUM_FF = j

                # Without Fake Food
                XML.USE_FF_DOS = "false"
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food: 0\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # With Fake Food
                XML.USE_FF_DOS = "true"
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food: {XML.NUM_FF}\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)
        elif i == 1:
            dmode = "Cluster"
            # Cluster
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Without Fake Food
                XML.USE_FF_DOS = "false"
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food Clusters: {XML.NUM_RCL}({XML.RCL_X}x{XML.RCL_Y}), Num Fake Food Clusters: 0\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # With Fake Food
                XML.USE_FF_DOS = "true"
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food Clusters: {XML.NUM_RCL}({XML.RCL_X}x{XML.RCL_Y}), Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)

        elif i == 2:
            dmode = "PowerLaw"
            # PowerLaw
            for j in num_plaw_ff:
                XML.NUM_PLAW_FF = j

                # Without Fake Food
                XML.USE_FF_DOS = "false"
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food: 0\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # With Fake Food
                XML.USE_FF_DOS = "true"
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_PLAW_RF}, Num Fake Food: {XML.NUM_PLAW_FF}\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)
        else:
            raise Exception("In 'MainExperiment()': Invalid distribution mode...\n\n")

def QZoneExperiment():
    run_count = 30

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1000
    XML.Densify(True)
    XML.USE_FF_DOS = "true"

    # Random Distribution Settings
    XML.NUM_RF = 108

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]
    
    # Powerlaw Distribution Settings
    XML.NUM_PLAW_RF = 108

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods (Real Food Only)
        XML.setDistribution(i)
        XML.FFD = 1
        print(f'QZone Experiment, {run_count} iterations Standard Density, {run_count} Increased Density\n')
        dmode = ""
        if i == 0:
            dmode = "Random Real Food"
            # Random
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Standard Density
                XML.UseQZone(False)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Increased Density
                XML.UseQZone(True)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)
        elif i == 1:
            dmode = "Cluster Real Food"
            # Cluster
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Standard Density
                XML.UseQZone(False)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food Clusters: {XML.NUM_RCL}({XML.RCL_X}x{XML.RCL_Y}), Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Increased Density
                XML.UseQZone(True)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food Clusters: {XML.NUM_RCL}({XML.RCL_X}x{XML.RCL_Y}), Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)

        elif i == 2:
            dmode = "PowerLaw Real Food"
            # PowerLaw
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Standard Density
                XML.UseQZone(False)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_PLAW_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Increased Density
                XML.UseQZone(True)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_PLAW_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)
        else:
            raise Exception("In 'MainExperiment()': Invalid distribution mode...\n\n")

def DensityExperiment():
    run_count = 30

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1000
    XML.USE_FF_DOS = "true"
    XML.UseQZone(False)

    # Random Distribution Settings
    XML.NUM_RF = 108

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]
    
    # Powerlaw Distribution Settings
    XML.NUM_PLAW_RF = 108

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods (Real Food Only)
        XML.setDistribution(i)
        XML.FFD = 1
        print(f'Density Experiment, {run_count} iterations standard density, {run_count} iterations increased density\n')
        dmode = ""
        if i == 0:
            dmode = "Random Real Food"
            # Random
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Standard Density
                XML.Densify(False)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Increased Density
                XML.Densify(True)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)
        elif i == 1:
            dmode = "Cluster Real Food"
            # Cluster
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Standard Density
                XML.Densify(False)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food Clusters: {XML.NUM_RCL}({XML.RCL_X}x{XML.RCL_Y}), Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Increased Density
                XML.Densify(True)
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food Clusters: {XML.NUM_RCL}({XML.RCL_X}x{XML.RCL_Y}), Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)

        elif i == 2:
            dmode = "PowerLaw Real Food"
            # PowerLaw
            for j in num_fcl:
                XML.NUM_FCL = j[0]
                XML.FCL_X = j[1]
                XML.FCL_Y = j[2]

                # Standard Density
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_PLAW_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Increased Density
                XML.createXML()
                for k in range(run_count):
                    print(f'Distribution: {dmode}, Iteration: {k+1}, Num Real Food: {XML.NUM_PLAW_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

                # Plot results
                Read(XML.fname_header+'DoSData.txt')
                Plot2(XML.fname_header)
        else:
            raise Exception("In 'MainExperiment()': Invalid distribution mode...\n\n")

def Experiment1():
    run_count = 30

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(True)  # Use standard density for fake food
    XML.setBotCount(16)
    XML.setDistribution(1) # Cluster Distribution Only

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]

    RFmax = XML.NUM_RCL*XML.RCL_X*XML.RCL_Y
    FFmax = num_fcl[len(num_fcl)-1][0]*num_fcl[len(num_fcl)-1][1]*num_fcl[len(num_fcl)-1][2]

    flist = []

    # Standard CPFA
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    flist.append(XML.setFname()+"DoSData.txt")
    XML.createXML()
    for j in range(run_count):
        print(f'Standard CPFA, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    
    for j in num_fcl:
        XML.NUM_FCL = j[0]
        XML.FCL_X = j[1]
        XML.FCL_Y = j[2]
        
        # w/ Fake Food
        XML.UseFFDoS(True)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            print(f'CPFA w/ Fake Food, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ QZones no merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 0
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            print(f'CPFA w/ QZones (no merge), Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ QZones distance-based merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 1
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            print(f'CPFA w/ QZones (DB-Merge), Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    PlotExp1(flist, RFmax, FFmax)

def Experiment1_v2(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(True)  # Use increased density for fake food
    XML.setBotCount(16)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.RD_PATH=f'results_Exp1_{run_count}it/'

    if (not CheckDirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not CheckDirectoryEmpty(XML.RD_PATH)):
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

    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]

    RFmax = XML.NUM_RCL*XML.RCL_X*XML.RCL_Y
    FFmax = num_fcl[len(num_fcl)-1][0]*num_fcl[len(num_fcl)-1][1]*num_fcl[len(num_fcl)-1][2]

    flist = []

    # Standard CPFA
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    flist.append(XML.setFname()+"DoSData.txt")
    XML.createXML()
    for j in range(run_count):
        time.sleep(0.05)
        print(f'Standard CPFA, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    
    for j in num_fcl:

        # pause for 5ms to check for termination command
        time.sleep(0.05)

        XML.NUM_FCL = j[0]
        XML.FCL_X = j[1]
        XML.FCL_Y = j[2]
        
        # w/ Fake Food
        XML.UseFFDoS(True)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            time.sleep(0.05)
            print(f'CPFA w/ Fake Food, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ QZones no merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 0
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            time.sleep(0.05)
            print(f'CPFA w/ QZones (no merge), Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ QZones distance-based merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 1
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            time.sleep(0.05)
            print(f'CPFA w/ QZones (DB-Merge), Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    PlotExp1_v2(flist, XML.RD_PATH, RFmax, FFmax)
    CheckForTerminatedSimulations(XML.RD_PATH)
    # PlotExp1_merge_test(flist, RFmax, FFmax)

def Experiment2_v1(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.Densify(True)  # Use standard density for fake food
    XML.setBotCount(16)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.RD_PATH=f'results_Exp2_{run_count}it/'

    if (not CheckDirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not CheckDirectoryEmpty(XML.RD_PATH)):
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

    XML.NUM_FCL = 3
    XML.FCL_X = 6
    XML.FCL_Y = 6

    RFmax = XML.NUM_RCL*XML.RCL_X*XML.RCL_Y
    FFmax = XML.NUM_FCL*XML.FCL_X*XML.FCL_Y

    # Vary sim time -> 10, 15, 20, 25, 30
    time = [10*60, 15*60, 20*60, 25*60, 30*60]

    flist = []

    for t in time:
        XML.MAX_SIM_TIME = t

        # Standard CPFA
        XML.UseFFDoS(False)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for j in range(run_count):
            print(f'Standard CPFA, Iteration: {j+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ Fake Food
        XML.UseFFDoS(True)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            print(f'CPFA w/ Fake Food, Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ QZones no merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 0
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            print(f'CPFA w/ QZones (no merge), Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # w/ QZones distance-based merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 1
        flist.append(XML.setFname()+"DoSData.txt")
        XML.createXML()
        for k in range(run_count):
            print(f'CPFA w/ QZones (DB-Merge), Iteration: {k+1}, Num Real Food: {XML.NUM_RF}, Num Fake Food Clusters: {XML.NUM_FCL}({XML.FCL_X}{XML.FCL_Y})\n')
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    PlotExp2_v1(flist, RFmax, FFmax)
    CheckForTerminatedSimulations(XML.RD_PATH)

def rePlotDensityExperiment():
    run_count = 30

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1000
    XML.USE_FF_DOS = "true"
    XML.UseQZone(False)

    # Random Distribution Settings
    XML.NUM_RF = 108
    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6
    
    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]
    # Powerlaw Distribution Settings
    XML.NUM_PLAW_RF = 108

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods
        XML.setDistribution(i)
        XML.FFD = 1

        for j in num_fcl:
            XML.NUM_FCL = j[0]
            XML.FCL_X = j[1]
            XML.FCL_Y = j[2]

            XML.setFname()

            # Plot results
            Read(XML.fname_header+'DoSData.txt')
            Plot2(XML.fname_header)
            VaryFFPlot2(XML.fname_header, j[0])

def rePlotExperiment1_v2(rc, rd_path):
    run_count = rc
    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.Densify(True)
    XML.setBotCount(16)
    XML.setDistribution(1)
    XML.RD_PATH = rd_path
    XML.UseFFOnly(False)

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6
    
    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]

    RFmax = XML.NUM_RCL*XML.RCL_X*XML.RCL_Y
    FFmax = num_fcl[len(num_fcl)-1][0]*num_fcl[len(num_fcl)-1][1]*num_fcl[len(num_fcl)-1][2]

    flist = []

    # Standard CPFA
    XML.UseFFDoS(False)
    XML.UseQZone(False)
    flist.append(XML.setFname()+"DoSData.txt")

    for j in num_fcl:
        XML.NUM_FCL = j[0]
        XML.FCL_X = j[1]
        XML.FCL_Y = j[2]
        
        # w/ Fake Food
        XML.UseFFDoS(True)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        
        # w/ QZones no merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 0
        flist.append(XML.setFname()+"DoSData.txt")

        # w/ QZones distance-based merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 1
        flist.append(XML.setFname()+"DoSData.txt")
        
    # PlotExp1(flist, RFmax, FFmax)
    PlotExp1_v2(flist, XML.RD_PATH, RFmax, FFmax)

def rePlotExperiment2_v1():
    run_count = 30

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.Densify(True)  # Use standard density for fake food
    XML.setBotCount(16)
    XML.setDistribution(1) # Cluster Distribution Only

    # Cluster Distribution Settings
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    XML.NUM_FCL = 3
    XML.FCL_X = 6
    XML.FCL_Y = 6

    RFmax = XML.NUM_RCL*XML.RCL_X*XML.RCL_Y
    FFmax = XML.NUM_FCL*XML.FCL_X*XML.FCL_Y

    # Vary sim time -> 10, 15, 20, 25, 30
    time = [10*60, 15*60, 20*60, 25*60, 30*60]

    flist = []

    for t in time:
        XML.MAX_SIM_TIME = t

        # Standard CPFA
        XML.UseFFDoS(False)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        
        # w/ Fake Food
        XML.UseFFDoS(True)
        XML.UseQZone(False)
        flist.append(XML.setFname()+"DoSData.txt")
        
        # w/ QZones no merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 0
        flist.append(XML.setFname()+"DoSData.txt")

        # w/ QZones distance-based merging
        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.MM = 1
        flist.append(XML.setFname()+"DoSData.txt")

    PlotExp2_v1(flist, RFmax, FFmax)

def PheromoneExperiment_v1(rc):
    run_count = rc

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 900
    XML.setBotCount(16)
    XML.setDistribution(1) # Cluster Distribution Only
    XML.RD_PATH=f'results_PhermoneExp1/'
    XML.UseFFOnly(True)
    XML.UseQZone(False)

    if (not CheckDirectoryExists(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} does not exist! Creating {XML.RD_PATH}...\n')
    if (not CheckDirectoryEmpty(XML.RD_PATH)):
        print(f'Directory {XML.RD_PATH} is not empty. Do you wish to clear the directory and continue? (y/n)')
        if (input() != 'y'):
            print('Aborting...')
            exit()
        else:
            ClearDirectory(XML.RD_PATH)

    # Cluster Distribution Settings
    XML.NUM_FCL = 3
    XML.FCL_X = 6
    XML.FCL_Y = 6

    FFmax = XML.NUM_FCL*XML.FCL_X*XML.FCL_Y

    flist = []

    XML.Densify(False)
    flist.append(XML.setFname()+"DoSData.txt")
    XML.createXML()
    for i in range(run_count):
        print(f'Running simulation {i+1}/{run_count}, Density: Standard')
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.Densify(True)
    flist.append(XML.setFname()+"DoSData.txt")
    XML.createXML()
    for i in range(run_count):
        print(f'Running simulation {i+1}/{run_count}, Density: Increased')
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")
    
def testVisual():

    XML = config.C_XML_CONFIG(1)

    XML.VISUAL = True
    XML.MAX_SIM_TIME = 900
    XML.Densify(True)
    XML.setBotCount(16)
    XML.UseAltDistribution(False)
    XML.setDistribution(1)
    XML.MM = 1

    for i in range (3):
        # Cluster Distribution Settings
        XML.NUM_RCL = 3
        XML.RCL_X = 6
        XML.RCL_Y = 6
        
        XML.NUM_FCL = 5
        XML.FCL_X = 6
        XML.FCL_Y = 6

        XML.UseFFDoS(True)
        XML.UseQZone(True)
        XML.createXML()
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def testExperiment1Visual():
    run_count = 1

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = True
    XML.MAX_SIM_TIME = 1000
    XML.Densify(True)

    XML.NUM_RF = 108
    XML.NUM_RCL = 3
    XML.RCL_X = 6
    XML.RCL_Y = 6

    XML.NUM_FCL = 1
    XML.FCL_X = 6
    XML.FCL_Y = 6

    num_fcl =   [(1,XML.FCL_X,XML.FCL_Y),(2,XML.FCL_X,XML.FCL_Y), (3,XML.FCL_X,XML.FCL_Y), 
                (4,XML.FCL_X,XML.FCL_Y), (5,XML.FCL_X,XML.FCL_Y)]
    
    # Powerlaw Distribution Settings
    XML.NUM_PLAW_RF = 108

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods (Real Food Only)
        XML.setDistribution(i)
        XML.FFD = 1

        
        for j in range(3):

            if j == 0:  # Standard CPFA
                XML.UseFFDoS(False)
                XML.UseQZone(False)
                XML.createXML()
                for k in range(run_count):
                    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

            if j == 1: # w/ Fake Food
                XML.UseFFDoS(True)
                XML.UseQZone(False)
                for k in num_fcl:
                    XML.NUM_FCL = k[0]
                    XML.FCL_X = k[1]
                    XML.FCL_Y = k[2]
                    XML.createXML()

                    for l in range(run_count):
                        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

            if j == 2: # w/ QZones
                XML.UseFFDoS(True)
                XML.UseQZone(True)
                for k in num_fcl:
                    XML.NUM_FCL = k[0]
                    XML.FCL_X = k[1]
                    XML.FCL_Y = k[2]
                    XML.createXML()

                    for l in range(run_count):
                        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def quickTest():
    
    run_count = 1

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = True
    XML.Densify(False)
    XML.UseQZone(False)
    XML.MAX_SIM_TIME = 1500
    XML.setDistribution(1)
    XML.DRAW_TRAILS = 1

    # XML.RANDOM_SEED=120678
    # XML.RANDOM_SEED=743490
    # XML.RANDOM_SEED=301421

    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def terminationTest(rc):
    run_count = rc
    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1500
    XML.setDistribution(1)
    XML.DRAW_TRAILS = 0
    XML.RANDOM_SEED = 120678
    XML.createXML()

    for i in range(run_count):
        time.sleep(0.25)
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    t_count = 0
    terminate = False
    with open(XML.fname_header+"TerminatedCount.txt") as f:
        for line in f.readlines():
            data = line.strip().split(',')
            for d in data:
                if d == 1:
                    t_count += 1
                    terminate = True
                    break
            if terminate: 
                break


    
    print(f'There were {t_count} terminations in total.\n')

def Experiment3TimeTest():
    XML = config.C_XML_CONFIG(1)

    XML.VISUAL = True
    XML.Densify(True)
    XML.setBotCount(16)
    XML.setDistribution(1)
    XML.UseAltDistribution(True)
    XML.ALT_FCL_W = 64
    XML.ALT_FCL_L = 8
    XML.UseFFDoS(True)
    XML.UseQZone(True)
    sim_time_list = (6*60,8*60,10*60,12*60)

    # Without merging
    XML.MM = 0
    for time in sim_time_list:
        XML.MAX_SIM_TIME = time
        XML.createXML()
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")
    
    # With merging
    XML.MM = 1
    for time in sim_time_list:
        XML.MAX_SIM_TIME = time
        XML.createXML()
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def CheckDirectoryExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True

def CheckDirectoryEmpty(path):
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

def CheckForTerminatedSimulations(path):
    # Read all files in path that end in "TerminatedCount.txt" for each run, check if any data contains a 0
    # If so, return True, else return False
    terminated_count = 0
    tfile_list = []
    for file in os.listdir(path):
        if file.endswith("TerminatedCount.txt"):
            with open(os.path.join(path, file)) as f:
                for line in f.readlines():
                    data = line.strip().split(',')
                    for d in data:
                        if d == '0':
                            terminated_count += 1
                            tfile_list.append(file)
                            break
    if terminated_count == 0:
        # remove all files that end with "TerminatedCount.txt"
        for file in os.listdir(path):
            if file.endswith("TerminatedCount.txt"):
                os.remove(os.path.join(path, file))
        return False
    else:
        print(f'Results are invalid. Termination Count: {terminated_count}\n')
        # print the list of filenames that resulted in 1 or more terminations
        for file in tfile_list:
            print(f'{file}\n')
        return True

# Random Seed List
# 
# 
# Pheromone waypoint bug: 120678
# 
# New merge with smaller radius bug: 743490
# 
# inf slope: 301421
# 
# Bot 22 stuck on south wall: 267451
# 

if __name__ == "__main__":

    # QZoneExperiment()
    # DensityExperiment()
    # rePlotDensityExperiment()
    # testVisual()

    # Experiment1_v2(60)
    rePlotExperiment1_v2(30,'results_Exp1/')
    # Experiment2_v1()

    # rePlotExperiment2_v1()
    # Experiment3TimeTest()
    # testExperiment1Visual()
    # Experiment1()
    # rePlotExperiment1_v2()











# ARCHIVED


def Plot1():

    TFC = np.array(TOTAL_FOOD_COLLECTED)
    TCR = np.array(TOTAL_COLLECTION_RATE)
    RFC = np.array(REAL_FOOD_COLLECTED)
    RCR = np.array(REAL_COLLECTION_RATE)
    FFC = np.array(FAKE_FOOD_COLLECTED)
    FCR = np.array(FAKE_COLLECTION_RATE)

    TFC_avg = np.zeros(shape=(2))
    TFC_avg[0] = np.mean(np.split(TFC.astype(float), 2)[0])
    TFC_avg[1] = np.mean(np.split(TFC.astype(float), 2)[1])
    TCR_avg = np.zeros(shape=(2))
    TCR_avg[0] = np.mean(np.split(TCR.astype(float), 2)[0])
    TCR_avg[1] = np.mean(np.split(TCR.astype(float), 2)[1])
    RFC_avg = np.zeros(shape=(2))
    RFC_avg[0] = np.mean(np.split(RFC.astype(float), 2)[0])
    RFC_avg[1] = np.mean(np.split(RFC.astype(float), 2)[1])
    RCR_avg = np.zeros(shape=(2))
    RCR_avg[0] = np.mean(np.split(RCR.astype(float), 2)[0])
    RCR_avg[1] = np.mean(np.split(RCR.astype(float), 2)[1])
    FFC_avg = np.zeros(shape=(2))
    FFC_avg[0] = np.mean(np.split(FFC.astype(float), 2)[0])
    FFC_avg[1] = np.mean(np.split(FFC.astype(float), 2)[1])
    FCR_avg = np.zeros(shape=(2))
    FCR_avg[0] = np.mean(np.split(FCR.astype(float), 2)[0])
    FCR_avg[1] = np.mean(np.split(FCR.astype(float), 2)[1])

    x_tick_labels = ['DoS Disabled', 'DoS Enabled']

    x = np.arange(len(x_tick_labels))
    barWidth = 0.35
    
    fig1, ax1 = plt.subplots()
    group1 = ax1.bar(x, RFC_avg, barWidth, label=x_tick_labels, color='black')
    ax1.set_xticks(x, x_tick_labels)
    ax1.set_ylabel('Collection Count')
    ax1.set_title('Real Food Collection Count Averages (10 iterations ea.)')
    ax1.bar_label(group1, padding=1)
    fig1.tight_layout()
    fig1.savefig("testfig_count.png")

    fig2, ax2 = plt.subplots()
    group2 = ax2.bar(x, RCR_avg, barWidth, label=x_tick_labels, color = 'black')
    ax2.set_xticks(x, x_tick_labels)
    ax2. set_ylabel('Collection Rate')
    ax2.set_title('Real Food Collection Rate Averages (10 iterations ea.)')
    ax2.bar_label(group2, padding=1)
    fig2.tight_layout()
    fig2.savefig('testfig_rate.png')

def Plot2(fname):

    # TFC = np.array(TOTAL_FOOD_COLLECTED)
    # TCR = np.array(TOTAL_COLLECTION_RATE)
    # RFC = np.array(REAL_FOOD_COLLECTED)
    # RCR = np.array(REAL_COLLECTION_RATE)
    FFC = np.array(FAKE_FOOD_COLLECTED)
    # FCR = np.array(FAKE_COLLECTION_RATE)

    # RFC_plt = np.array_split(RFC.astype(float), 2)
    FFC_plt = np.array_split(FFC.astype(float), 2)
    # RCR_plt = np.split(RCR.astype(float), 2)

    # print(f'{RFC_plt}')
    print(f'{FFC_plt}')

    x_tick_labels = ['Standard \nDensity', 'Increased \nDensity']
    
    # create boxplot for Real Food Count
    # bp1 = plt.boxplot(RFC_plt, vert=1)
    bp1 = plt.boxplot(FFC_plt, vert=1)
    ax = plt.gca()
    ax.set_ylabel('Collected (Fake) Resources')

    #### temporary change to match CURRENT real food total 128 ####

    # plt.yticks(range(0,257,32),['0','32','64','96','128','160','192','224','256'])
    # plt.yticks(range(0,129,16),['0','16','32','48','64','80','96','112','128']) 
    plt.yticks(range(0,109,12),['0','12','24','36','48','60','72','84','96','108']) 

    plt.xticks([1,2], x_tick_labels)
    # ax.set_title('Real Food Collection Count (50 iterations ea.)')
    # plt.savefig(fname+"_BOXPLOT.png")
    plt.savefig(fname+"_FF-BOXPLOT.png")

    plt.clf()
    plt.cla()
    
    # Print boxplot number data
    medians1 =  [round(item.get_ydata()[0],3) for item in bp1['medians']]
    means1 =    [round(item.get_ydata()[0],3) for item in bp1['means']]
    mins1 =     [round(item.get_ydata()[0],3) for item in bp1['caps']][::2]
    maxs1 =     [round(item.get_ydata()[0],3) for item in bp1['caps']][1::2]
    Qone1 =     [round(min(item.get_ydata()),3) for item in bp1['boxes']]
    Qthree1 =   [round(max(item.get_ydata()),3) for item in bp1['boxes']]

    fliers1 = [item.get_ydata() for item in bp1['fliers']]
    lo_out1 = []
    up_out1 = []
    for i in range(len(fliers1)):
        lower_outliers_by_box = []
        upper_outliers_by_box = []
        for outlier in fliers1[i]:
            if outlier < Qone1[i]:
                lower_outliers_by_box.append(round(outlier, 3))
            else:
                upper_outliers_by_box.append(round(outlier, 3))
        lo_out1.append(lower_outliers_by_box)
        up_out1.append(upper_outliers_by_box)\
    
    # with open(fname+"_BP-DATA.txt",'w') as f:
    with open(fname+"_FF-BP-DATA.txt",'w') as f:
    
        print  (f'*** {fname} BoxPlot Data ***\n\n'
                f'Key: [DoS Disabled, Dos Enabled]\n\n'
                f'Medians: {medians1}\n'
                f'Means: {means1}\n'
                f'Minimums: {mins1}\n'
                f'Maximums: {maxs1}\n'
                f'Quarter One: {Qone1}\n'
                f'Quarter Three: {Qthree1}\n'
                f'Lower Outliers: {lo_out1}\n'
                f'Upper Outliers: {up_out1}\n', file=f)

def VaryFFPlot2(fname, numFFC):

    # TFC = np.array(TOTAL_FOOD_COLLECTED)
    # TCR = np.array(TOTAL_COLLECTION_RATE)
    # RFC = np.array(REAL_FOOD_COLLECTED)
    # RCR = np.array(REAL_COLLECTION_RATE)
    FFC = np.array(FAKE_FOOD_COLLECTED)
    # FCR = np.array(FAKE_COLLECTION_RATE)

    # RFC_plt = np.array_split(RFC.astype(float), 2)
    FFC_plt = np.array_split(FFC.astype(float), 2)
    # RCR_plt = np.split(RCR.astype(float), 2)

    x_tick_labels = ['Standard \nDensity', 'Increased \nDensity']
    
    # create boxplot for Real Food Count
    # bp1 = plt.boxplot(RFC_plt, vert=1)
    bp1 = plt.boxplot(FFC_plt, vert=1)
    ax = plt.gca()
    ax.set_ylabel('Collected (Fake) Resources')

    #### temporary change to match CURRENT real food total 128 ####

    # plt.yticks(range(0,257,32),['0','32','64','96','128','160','192','224','256'])
    # plt.yticks(range(0,129,16),['0','16','32','48','64','80','96','112','128']) 
    # plt.yticks(range(0,109,12),['0','12','24','36','48','60','72','84','96','108'])

    if numFFC == 1: 
        plt.yticks(range(0,37,3),['0','3','6','9','12','15','18','21','24','27','30','33','36'])
    elif numFFC == 2:
        plt.yticks(range(0,73,6),['0','6','12','18','24','30','36','42','48','54','60','66','72'])
    elif numFFC == 3:
        plt.yticks(range(0,109,12),['0','12','24','36','48','60','72','84','96','108'])
    elif numFFC == 4:
        plt.yticks(range(0,145,12),['0','12','24','36','48','60','72','84','96','108','120','132','144'])
    elif numFFC == 5:
        plt.yticks(range(0,181,18),['0','18','36','54','72','90','108','126','144','162','180'])

    plt.xticks([1,2], x_tick_labels)
    # ax.set_title('Real Food Collection Count (50 iterations ea.)')
    # plt.savefig(fname+"_BOXPLOT.png")
    plt.savefig(fname+"_FF-BOXPLOT.png")

    plt.clf()
    plt.cla()
    
    # Print boxplot number data
    medians1 =  [round(item.get_ydata()[0],3) for item in bp1['medians']]
    means1 =    [round(item.get_ydata()[0],3) for item in bp1['means']]
    mins1 =     [round(item.get_ydata()[0],3) for item in bp1['caps']][::2]
    maxs1 =     [round(item.get_ydata()[0],3) for item in bp1['caps']][1::2]
    Qone1 =     [round(min(item.get_ydata()),3) for item in bp1['boxes']]
    Qthree1 =   [round(max(item.get_ydata()),3) for item in bp1['boxes']]

    fliers1 = [item.get_ydata() for item in bp1['fliers']]
    lo_out1 = []
    up_out1 = []
    for i in range(len(fliers1)):
        lower_outliers_by_box = []
        upper_outliers_by_box = []
        for outlier in fliers1[i]:
            if outlier < Qone1[i]:
                lower_outliers_by_box.append(round(outlier, 3))
            else:
                upper_outliers_by_box.append(round(outlier, 3))
        lo_out1.append(lower_outliers_by_box)
        up_out1.append(upper_outliers_by_box)\
    
    # with open(fname+"_BP-DATA.txt",'w') as f:
    with open(fname+"_FF-BP-DATA.txt",'w') as f:
    
        print  (f'*** {fname} BoxPlot Data ***\n\n'
                f'Key: [DoS Disabled, Dos Enabled]\n\n'
                f'Medians: {medians1}\n'
                f'Means: {means1}\n'
                f'Minimums: {mins1}\n'
                f'Maximums: {maxs1}\n'
                f'Quarter One: {Qone1}\n'
                f'Quarter Three: {Qthree1}\n'
                f'Lower Outliers: {lo_out1}\n'
                f'Upper Outliers: {up_out1}\n', file=f)

# FROM OLD EXPERIMENT USING ALL COMBINATIONS OF DISTRIBUTION METHODS

    # dist = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

    # for d in dist:
    #     XML.RFD=d[0]
    #     XML.FFD=d[1]
    #     XML.USE_FF_DOS = "false"
    #     XML.createXML()
    #     for i in range(run_count):
    #         os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")
    #     XML.USE_FF_DOS = "true"
    #     XML.createXML()
    #     for i in range(run_count):
    #         os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    # def testPlot(fname):
    # # TFC = np.array(TOTAL_FOOD_COLLECTED)
    # # TCR = np.array(TOTAL_COLLECTION_RATE)
    # # RFC = np.array(REAL_FOOD_COLLECTED)
    # # RCR = np.array(REAL_COLLECTION_RATE)
    # FFC = np.array(FAKE_FOOD_COLLECTED)
    # # FCR = np.array(FAKE_COLLECTION_RATE)

    # # RFC_plt = np.array_split(RFC.astype(float), 2)
    # FFC_plt = np.array_split(FFC.astype(float), 2)
    # # RCR_plt = np.split(RCR.astype(float), 2)

    # print(f'{FFC_plt[0].size, FFC_plt[1].size}')

    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax.boxplot(FFC_plt, showfliers=False)
    # ax.set_xticklabels(['Standard Density', 'High Density'])
    # ax.set_ylabel('Food Collected')
    # ax.set_xlabel('Density')
    # ax.set_title('Food Collected vs. Density')
    # plt.savefig(fname+"_FF-BOXPLOT.png")
    # plt.close()