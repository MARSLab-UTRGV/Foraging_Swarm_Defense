import DoS_xml_config as config
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
np.set_printoptions(suppress=True)

SIM_TIME = []
TOTAL_FOOD_COLLECTED = []
TOTAL_COLLECTION_RATE = []
REAL_FOOD_COLLECTED = []
REAL_COLLECTION_RATE = []
FAKE_FOOD_COLLECTED = []
FAKE_COLLECTION_RATE = []

def Read(fname):
    count = 0
    with open("test.txt") as f:
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

# Bar Plot
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

# Box Plot
def Plot2(fname):

    # TFC = np.array(TOTAL_FOOD_COLLECTED)
    # TCR = np.array(TOTAL_COLLECTION_RATE)
    RFC = np.array(REAL_FOOD_COLLECTED)
    # RCR = np.array(REAL_COLLECTION_RATE)
    # FFC = np.array(FAKE_FOOD_COLLECTED)
    # FCR = np.array(FAKE_COLLECTION_RATE)

    RFC_plt = np.array_split(RFC.astype(float), 2)
    # RCR_plt = np.split(RCR.astype(float), 2)

    # print(f'{RFC_plt}')

    x_tick_labels = ['DoS \nDisabled', 'DoS \nEnabled']
    
    # create boxplot for Real Food Count
    bp1 = plt.boxplot(RFC_plt, vert=1)
    ax = plt.gca()
    ax.set_ylabel('Collected Resources')

    #### temporary change to match CURRENT real food total 128 ####

    # plt.yticks(range(0,257,32),['0','32','64','96','128','160','192','224','256'])
    plt.yticks(range(0,257,32),['0','16','32','48','64','80','96','112','128']) 


    plt.xticks([1,2], x_tick_labels)
    # ax.set_title('Real Food Collection Count (50 iterations ea.)')
    plt.savefig(fname+"_BOXPLOT.png")

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
    
    with open(fname+"_BP-DATA.txt",'w') as f:
    
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

def SimpleExperiment():
    run_count = 50

    XML = config.C_XML_CONFIG(run_count)

    XML.VISUAL = False
    XML.setDistribution(1) # Cluster Distribution

    XML.USE_FF_DOS = "false"
    XML.createXML()
    
    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.USE_FF_DOS = "true"
    XML.createXML()

    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def MainExperiment():
    run_count = 50

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1500

    # Random Distribution Settings
    XML.NUM_RF = 128
    XML.NUM_FF = 128
    # Cluster Distribution Settings
    XML.NUM_RCL = 2
    XML.NUM_FCL = 2
    # Powerlaw Distribution Settings
    XML.NUM_PLAW_RF = 128
    XML.NUM_PLAW_FF = 128

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods
        XML.setDistribution(i)

        # Without Fake Food
        XML.USE_FF_DOS = "false"
        XML.createXML()
        for j in range(run_count):
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # With Fake Food
        XML.USE_FF_DOS = "true"
        XML.createXML()
        for j in range(run_count):
            os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

        # Plot results
        Read(XML.fname_header+'DoSData.txt')
        Plot2(XML.fname_header)

def rePlot():
    run_count = 50

    XML = config.C_XML_CONFIG(run_count)
    XML.VISUAL = False
    XML.MAX_SIM_TIME = 1500

    for i in reversed(range(3)): # start with powerlaw
        # Go through all distribution methods
        XML.setDistribution(i)

        XML.setFname()

        # Plot results
        Read(XML.fname_header+'DoSData.txt')
        Plot2(XML.fname_header)

def testVisual():

    XML = config.C_XML_CONFIG(1)

    XML.VISUAL = True
    XML.MAX_SIM_TIME = 1500
    
    # Random Distribution Settings
    XML.NUM_RF = 128
    XML.NUM_FF = 128
    # Cluster Distribution Settings
    XML.NUM_RCL = 2     # 8x8 clusters
    XML.NUM_FCL = 2     # 8x8 clusters
    # Power Law Districution Settings
    XML.NUM_PLAW_RF = 128
    XML.NUM_PLAW_FF = 128

    XML.setDistribution(0)
    XML.USE_FF_DOS="false"
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.setDistribution(0)
    XML.USE_FF_DOS="true"
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.setDistribution(1)
    XML.USE_FF_DOS="false"
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.setDistribution(1)
    XML.USE_FF_DOS="true"
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.setDistribution(2)
    XML.USE_FF_DOS="false"
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.setDistribution(2)
    XML.USE_FF_DOS="true"
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")


if __name__ == "__main__":

    # SimpleExperiment()

    # Read("cluster_r24_50it.txt")
    # # Plot1()
    # Plot2("bp_test")

    # rePlot()

    testVisual()

    # MainExperiment()










# ARCHIVED





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