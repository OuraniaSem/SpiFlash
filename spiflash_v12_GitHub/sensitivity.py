import matplotlib.pyplot as plt
from scipy.stats import norm
import ast
import json
import os
import pandas as pd
from main_function_Sp import catch_info_xls

#------------------------------------------------------ SPECIFIC FUNCTION SENSITIVITY TRACE ------------------------------------------------------

def catch_bar_json(directory_name):
    myFile_json = str(directory_name) + "/infoBarplot.json"
    with open(myFile_json, "r") as read_file:
        info_json_bar = json.load(read_file)

    return info_json_bar

def catch_psycho_json(directory_name):
    myFile_json = str(directory_name) + "/infoPyscho.json"
    with open(myFile_json, "r") as read_file:
        info_json_psycho = json.load(read_file)

    return info_json_psycho

def plot_sensitivity(liste_sensitivity, liste_frequence_amplitude):

    plt.rcParams.update({'font.size': 10})
    plt.rcParams["figure.figsize"] = (10,4)


    fig, axs = plt.subplots(1)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.plot(liste_frequence_amplitude, liste_sensitivity)
    
    axs.legend(loc='best')

    plt.tight_layout()
    plt.show()

#------------------------------------------------------ MAIN FUNCTION PART ------------------------------------------------------
def main_sensitivity(xl_path):
    # get the info from the excell file
    my_data_xls, my_dirname = catch_info_xls(xl_path) 
    info_bar_json = catch_bar_json(my_dirname)

    info_psy_json = catch_psycho_json(my_dirname)

    print(info_bar_json)
    print(info_psy_json[0])
    print(info_psy_json[1])

    info_hit_amp =  info_psy_json[0]
    info_miss_amp = info_psy_json[1]

    liste_s = []
    liste_amp_freq = []
    false_alarm_rate = (info_bar_json[0]["NOgo_false alarm"] / (info_bar_json[0]["NOgo_false alarm"] + info_bar_json[0]["NOgo_rejection"]))
    if false_alarm_rate == 1:
        false_alarm_rate = 0.99
    if false_alarm_rate == 0:
        false_alarm_rate = 0.01
    print(false_alarm_rate)

    for (key1, value1), (key2, value2) in zip (info_hit_amp.items(), info_miss_amp.items()):
        miss = value2 - value1
        print(miss)
        hit_rate = (value1 / (value1 + miss))
        if hit_rate == 1:
            hit_rate = 0.99
        if hit_rate == 0:
            hit_rate = 0.01
        print(hit_rate)

        s = (norm.ppf(hit_rate)) - (norm.ppf(false_alarm_rate))
        s = float("{:.3f}".format(s))
        liste_s.append(s)
        print(key1)
        liste_amp_freq.append(ast.literal_eval(key1))
        print(s)

    print(liste_s)
    print(liste_amp_freq)

    return liste_s, liste_amp_freq