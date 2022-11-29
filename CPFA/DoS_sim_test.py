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

def PlotResults():

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

def SimpleExperiment():
    run_count = 10

    XML = config.C_XML_CONFIG()

    XML.VISUAL = False

    # Both set to clustered distribution
    XML.RFD = 1
    XML.FFD = 1

    XML.USE_FF_DOS = "false"
    XML.createXML()
    
    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.USE_FF_DOS = "true"
    XML.createXML()

    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def getSnapshots():

    XML = config.C_XML_CONFIG()

    XML.VISUAL = True

    XML.RFD = 0
    XML.FFD = 0
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 0
    XML.FFD = 1
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 0
    XML.FFD = 2
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 1
    XML.FFD = 0
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 1
    XML.FFD = 1
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 1
    XML.FFD = 2
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 2
    XML.FFD = 0
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 2
    XML.FFD = 1
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    XML.RFD = 2
    XML.FFD = 2
    
    XML.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")


if __name__ == "__main__":

    # SimpleExperiment()
    # getSnapshots()

    Read("test.txt")
    PlotResults()