#!/usr/bin/env python3
import matplotlib.pyplot as plt
import sys
import numpy as np

def get_perf_dict(perf):
    '''The function get_lists takes in input a file containing the evaluation of the performance.
    The file is organised in a fasta file fashion: a line for the threshold, identified with the ">" character,
    and the following line containing TP, TN, FN, FP, q2 (accuracy), MCC. '''
    with open(perf, "r") as input_f:
        perf_dict = {}
        mccs = []
        ths = []
        for line in input_f:
            line = line.rstrip()
            if ">" in line:
                ths.append(float(line.split()[1]))
            elif ":" not in line : 
                mcc = line.split(",")[5] # mcc = val
                mccs.append(float(mcc.split("=")[1]))
        for i in range(len(mccs)):
            perf_dict[ths[i]] = mccs[i]
    return perf_dict

def best_th(perf_dict):
    '''The function takes in input a dictionary with key-val pairs that are thresholds and mcc values , and returns the 
    threshold value that maximise the mcc.'''
    max_mcc = 0
    best_th = 0
    for key,val in perf_dict.items():
        if val >= max_mcc:
            max_mcc = val
            best_th = key
    return float(best_th)

def plot_mcc_values(thresholds, mcc_values, filename):
    """Plot MCC values against threshold values."""
    plt.plot(thresholds, mcc_values, marker='o', linestyle='-')
    plt.xscale('log')  # Imposta l'asse x su scala logaritmica
    plt.xlabel('Threshold')
    plt.ylabel('MCC Value')
    plt.title('MCC Values for Different Thresholds')
    plt.grid(True)  
    # Formattazione personalizzata per le etichette sull'asse x

    plt.xticks(thresholds, ['10^{}'.format(int(np.log10(t))) for t in thresholds], rotation=45)

    plt.savefig(filename)

if __name__=="__main__":
    perf = sys.argv[1]
    perf_dict =  get_perf_dict(perf)
    print(best_th(perf_dict))


    output_image = sys.argv[2]

    # Define threshold values and corresponding MCC values
    mccs = []
    ths = []
    for key, val in perf_dict.items():
        mccs.append(float(val))
        ths.append(float(key))

    # Plot the MCC values
    plot_mcc_values(ths, mccs, output_image)

    