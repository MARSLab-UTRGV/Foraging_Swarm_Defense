import DoS_xml_config_base as config
import os
import matplotlib.pyplot as plt
from datetime import datetime

# def read(fname):

# def plot(plt_fname):

# def getFilenames():

if __name__ == "__main__":
    # txt_fname,plt_fname = getFilenames()

    config.createXML()

    run_count = 1
    
    for i in range(run_count):
        os.system("argos3 -c ./experiments/CPFA_DoS_Simulation.xml")