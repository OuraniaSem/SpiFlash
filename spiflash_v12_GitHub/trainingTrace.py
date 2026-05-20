"""
Alexandre CORNIER - 09/09/2021 - trainingTrace.py

This code allow us to get 2 traces to represent the hit percentage and timeout percentage throughout the session.
For that, we create a a dictionnary like this {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, 'NOgo_false alarm' : 0, "NOgo_rejection" : 0, 'NOgo_timeout_paw' : 0}
like the barplot script, but every 20 trials (we can change this number also) we save the current dictionnary with the number of events that we have identified
And then we create new dictionnaries until the end of experiments every 20 trials.

"""
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
from main_function_Sp import catch_info_xls, catch_info_json, search_nb_newtrial, search_nb_endtrial, diff_new_end_trial, case_if_stim, case_if_NO_stim, get_title

#------------------------------------------------------ SPECIFIC FUNCTION TRAINING TRACE ------------------------------------------------------
#return the info of the file data_event
def catch_info_data_envent_full(directory_name):
    myFile_json = str(directory_name) + "/data_event_full.json"
    with open(myFile_json, "r") as read_file:
        info_json = json.load(read_file)

    return info_json

# Save the dictionnary with all the event in a json format
def save_eventDico_json(the_dico, directory_name):
    with open(str(directory_name) + '/data_event_full.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)


def save_infoTraining_json(the_dico, directory_name):
    with open(str(directory_name) + '/infoTraining.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)

def plot_things_training(x_names, percent_hit, percent_timeout, my_title_plot, dir_name):

    linear_model_hit=np.polyfit(x_names,percent_hit,2)
    linear_model_fn_hit=np.poly1d(linear_model_hit)
    linear_model_timeout=np.polyfit(x_names,percent_timeout,2)
    linear_model_fn_timeout=np.poly1d(linear_model_timeout)
    x_s=np.arange(0,x_names[-1])
    

    plt.rcParams.update({'font.size': 16})
    plt.rcParams["figure.figsize"] = (8,6)
    
    titleHit = 'Training trace Hit ' + str(my_title_plot)
    titleTimeout = 'Training trace Timeout ' + str(my_title_plot)


    fig, axs = plt.subplots(2)

    if "wt" in my_title_plot:
        axs[0].plot(x_names, percent_hit,"o", color="green", label = "Hit")
        axs[0].plot(x_s,linear_model_fn_hit(x_s),color="green", label = "Fit Hit")
    else:
        axs[0].plot(x_names, percent_hit,"o", color="blue", label = "Hit")
        axs[0].plot(x_s,linear_model_fn_hit(x_s),color="blue", label = "Fit Hit")
        
    axs[1].plot(x_names, percent_timeout, "o", color="orange", label = "Timeout")
    axs[1].plot(x_s,linear_model_fn_timeout(x_s),color="red", label = "Fit Timeout")

    axs[0].title.set_text(titleHit)
    axs[0].set_xlabel('Number of trials')
    axs[0].set_ylabel('Hit (%)')
    axs[1].title.set_text(titleTimeout)
    axs[1].set_xlabel('Number of trials')
    axs[1].set_ylabel('Timeout (%)')

    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)

    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    axs[0].set_ylim([0, 100])
    axs[1].set_ylim([0, 100])

    plt.tight_layout()
    fig.savefig(str(dir_name) + "/TrainingTrace.svg")
    plt.show()

#------------------------------------------------------ MAIN PART ------------------------------------------------------
def main_training(xl_path):
    # get the info from the excell file
    my_data_xls, my_dirname = catch_info_xls(xl_path) 
    # get the info from json file
    my_data_json = catch_info_json(my_dirname)
    number_trial = len(my_data_json)
    # create a global list
    liste_hfmr = []
    # dictionnary with all the info (hit, miss, GO timeout, false alarm, rejection)
    hfmr_dico = {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, 'NOgo_false alarm' : 0, "NOgo_rejection" : 0, 'NOgo_timeout_paw' : 0}
    Liste_total_trial_go = []
    Liste_total_trial_NOgo = []

    liste_newtrial = search_nb_newtrial(my_data_xls, number_trial) # get the line  new trial
    liste_endtrial = search_nb_endtrial(my_data_xls, number_trial) # get the line of the end trial
    my_liste_diff = diff_new_end_trial(liste_newtrial, liste_endtrial) # get the range between new trial and end trial

    # use this as a conteur for the global list
    about_trial_20 = 0

    #loop to check all the information from the different trial
    for icount_liste_nbTrial in range (len(liste_newtrial)):
        about_trial_20 += 1
        if my_data_json[icount_liste_nbTrial].get('trial_type') == "Go" :
            case_if_stim(hfmr_dico, my_liste_diff, my_data_xls, liste_newtrial, icount_liste_nbTrial)
        elif my_data_json[icount_liste_nbTrial].get('trial_type') == "Nogo" :
            case_if_NO_stim(hfmr_dico, my_liste_diff, my_data_xls, liste_newtrial, icount_liste_nbTrial)

        if about_trial_20 == 10 :
            liste_hfmr.append(hfmr_dico)
            wait_trial_total_go = hfmr_dico["GO_hit" ] + hfmr_dico["GO_miss"] + hfmr_dico["GO_timeout"]
            Liste_total_trial_go.append(wait_trial_total_go)
            wait_trial_total_NOgo = hfmr_dico['NOgo_false alarm'] + hfmr_dico["NOgo_rejection"] + hfmr_dico['NOgo_timeout_paw']
            Liste_total_trial_NOgo.append(wait_trial_total_NOgo)
            hfmr_dico = {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, 'NOgo_false alarm' : 0, "NOgo_rejection" : 0, 'NOgo_timeout_paw' : 0}
            wait_trial_total = 0
            wait_trial_total_NOgo = 0
            about_trial_20 = 0

    print(liste_hfmr)
    print(liste_newtrial)
    print("bonjour")
    print(Liste_total_trial_go)
    print(Liste_total_trial_NOgo)

    # boolean fo if you want to save the file, so turn to True
    save_ListMyDico = True
    if save_ListMyDico == True :
        save_eventDico_json(liste_hfmr, my_dirname)

    #get info from "data_event_full.json"
    data_event = catch_info_data_envent_full(my_dirname)
    print(data_event)

    liste_x_names = []
    for i in range(0, len(liste_newtrial), 10):
        i+= 10
        liste_x_names.append(i)

    x_names = np.array(liste_x_names)

    liste_x_values = []
    pourcent_x_values_hit = []
    pourcent_x_values_timeout = []

    for icount_liste in range(len(data_event)):
        x_values = data_event[icount_liste]["GO_hit"]
        liste_x_values.append(x_values)
        final_results = (x_values*100) / Liste_total_trial_go[icount_liste]
        final_results = float("{:.2f}".format(final_results))
        pourcent_x_values_hit.append(final_results)

    for icount_liste in range(len(data_event)):
        x_values = data_event[icount_liste]["GO_timeout"]
        liste_x_values.append(x_values)
        final_results = (x_values*100) / Liste_total_trial_go[icount_liste]
        final_results = float("{:.2f}".format(final_results))
        pourcent_x_values_timeout.append(final_results)

    print(x_names)
    print("Hit ", pourcent_x_values_hit)
    print("Timeout", pourcent_x_values_timeout)

    title_plot = get_title(my_data_xls)

    big_info = [pourcent_x_values_hit, pourcent_x_values_timeout]

    save_myDico = True
    if save_myDico == True :
        save_infoTraining_json(big_info, my_dirname)

    return x_names, pourcent_x_values_hit, pourcent_x_values_timeout, title_plot, my_dirname