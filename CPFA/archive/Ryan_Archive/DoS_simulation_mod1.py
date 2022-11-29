import DoS_xml_config_mod1 as config
import os
import matplotlib.pyplot as plt
from datetime import datetime

VISUAL =            False                    # turn on/off visual simulator

# Fake Food Loop Function Settings **
USE_FF_DOS =        "true"                  # Turn on/off fake_food DoS
FFD =               0                       # Fake Food Distribution Mode (0=Random, 1=Cluster, 2=PowerLaw)
NUM_FF =            32                      # Number of fake food to distribute for random distribution
NUM_FCL =           2                       # Number of fake food clusters for cluster distribution
FCL_X =             8                       # Fake cluster width X for cluster distribution
FCL_Y =             8                       # Fake cluster width Y for cluster distribution
NUM_PLAW_FF =       128                     # Number of fake food to distribute for power law distribution

# Real Food Loop Function Settings
RFD =               0                       # Real Food Distribution Mode (0=Random, 1=Cluster, 2=PowerLaw)
NUM_RF =            128                      # Number of real food to distribute for random distribution
NUM_RCL =           4                       # Number of real food clusters for cluster distribution
RCL_X =             8                       # Real cluster width X for cluster distribution
RCL_Y =             8                       # Real cluster width Y for cluster distribution
NUM_PLAW_RF =       256                     # Number of real food to distribute for power law distribution

# def read(fname):

# def plot(plt_fname):

# def getFilenames():

def updateConfigParams():
    config.setParams(USE_FF_DOS, FFD, NUM_FF, NUM_FCL, FCL_X, FCL_Y, NUM_PLAW_FF, RFD, NUM_RF, NUM_RCL, RCL_X, RCL_Y, NUM_PLAW_RF, VISUAL)

def SimpleExperiment():
    run_count = 10

    USE_FF_DOS = "false"
    updateConfigParams()
    config.createXML()
    
    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    USE_FF_DOS = "true"
    updateConfigParams()
    config.createXML()

    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

def getSnapshots():

    VISUAL = True

    RFD = 0
    FFD = 0
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 0
    FFD = 1
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 0
    FFD = 2
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 1
    FFD = 0
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 1
    FFD = 1
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 1
    FFD = 2
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 2
    FFD = 0
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 2
    FFD = 1
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")

    RFD = 2
    FFD = 2
    updateConfigParams()
    config.createXML()
    os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")


if __name__ == "__main__":

    # SimpleExperiment()
    getSnapshots()