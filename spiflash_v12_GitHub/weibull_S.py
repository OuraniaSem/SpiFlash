import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import psignifit as ps
import ast
from main_function_Sp import catch_info_xls, catch_info_json, search_nb_newtrial, search_nb_endtrial, liste_freq_amp, diff_new_end_trial, get_title


#------------------------------------------------------ SPECIFIC FUNCTION WEIBULL TRACE ------------------------------------------------------
#return a dicotionnary with the different event (hit, miss, go_timeout) just in case of a GO event from the json file
#input :
#   - dicotionnary with all the event at 0 at the beginning
#   - list with the range between new trial and end trial to catch the if there is a timeout or a reward event
#   - dataset from excell file
#   - list index of all the trial (specifics lines)
#   - a counteur 
def case_if_stim(the_dico, the_liste_diff, data_xls, the_liste_newTrial, counteur,
dataset_json, frequency_dico_hit, frequency_dico_miss, my_liste_freq_amp):
    my_hit = False
    my_timeout = False
    for i in range (the_liste_diff[counteur]):
        #print the currently line
        print(data_xls.iloc[the_liste_newTrial[counteur]][4])

        if data_xls.iloc[the_liste_newTrial[counteur]][4] == "Reward" :
            print("It's a HIT !")
            my_hit = True
            the_dico["GO_hit"] += 1

            for icount_liste in my_liste_freq_amp :
                if dataset_json[counteur].get('amp') == icount_liste or dataset_json[counteur].get('freq') == icount_liste:
                    frequency_dico_hit[icount_liste] += 1
            break
        
        elif data_xls.iloc[the_liste_newTrial[counteur]][4] == "Timeout" :
            print("There is a timeout!")
            my_timeout = True
            the_dico["GO_timeout"] += 1
            break

        #if the conditions are not good we will go the next line
        else :
            the_liste_newTrial[counteur] += 1
            i += 1

    #in case in all the trial there is no reward event or timeout event, it's a miss because there is a stimuli but not action from the mouse
    if my_hit == False and my_timeout == False :
        print("There is no lick event during a Go, it's a MISS !")
        the_dico["GO_miss"] += 1

        for icount_liste in my_liste_freq_amp :
            if dataset_json[counteur].get('amp') == icount_liste or dataset_json[counteur].get('freq') == icount_liste:
                frequency_dico_miss[icount_liste] += 1
    
    print('TRIAL NUMBER : ', counteur)
    print (the_dico)
    print('\n')
    return frequency_dico_hit, frequency_dico_miss

#return a dicotionnary with the different event (false alarm, rejection) just in case of a NOGO event from the json file
#input :
#   - dicotionnary with all the event at 0 at the beginning
#   - list with the range between new trial and end trial to catch the if there is a timeout or a reward event
#   - dataset from excell file
#   - list index of all the trial (specifics lines)
#   - a counteur 
def case_if_NO_stim(the_dico, the_liste_diff, data_xls, the_liste_newTrial, counteur):
    my_false_alarm = False
    my_timeout_pawoff = False
    for i in range (the_liste_diff[counteur]):
        #print the current line in the excell file between new trial and end trial
        print(data_xls.iloc[the_liste_newTrial[counteur]][4])

        if data_xls.iloc[the_liste_newTrial[counteur]][4] == "Timeout" :
            print("there is a timeout!")
            the_liste_newTrial[counteur] -= 1
            #HERE we check if this a timeout from the paw off or if the mouse break the beam before the stimuli
            if data_xls.iloc[the_liste_newTrial[counteur]][4] == 94 : # 94 => Port1In, so mouse break the beam but it's before the stimuli
                my_false_alarm = True
                the_dico["NOgo_false alarm"] += 1
                break
            
            elif data_xls.iloc[the_liste_newTrial[counteur]][4] == 93 : # 93 => BNC2Low, mouse took his paw off from the piezo
                my_timeout_pawoff = True
                the_dico['NOgo_timeout_paw'] += 1
                break

            the_liste_newTrial[counteur] += 1

        else :
            the_liste_newTrial[counteur] += 1
            i += 1

    if my_false_alarm == False and my_timeout_pawoff == False :
        the_dico["NOgo_rejection"] += 1

    
    print('TRIAL NUMBER : ', counteur + 1)
    print (the_dico)
    print('\n')
    return the_dico

def save_eventDico_json(the_dico,  directory_name):
    with open(str(directory_name) + '/infoWeibull.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)

def plot_things_weibull(liste_hit_rate, liste_amp):
    data = []

    for i in range(len(liste_amp)):
        little_liste = []
        little_liste.append(liste_amp[i])
        prct_100 = liste_hit_rate[i] * 100
        little_liste.append(prct_100)
        the_max = max(liste_hit_rate) * 100
        little_liste.append(the_max)
        data.append(little_liste)

    # set up a dictionnary and then set up the options
    options = dict()
    options['sigmoidName'] = 'weibull' # choose a cumulative Gauss as the sigmoid  
    options['expType']     = 'YesNo'   # YesNo experiments with two independent free asymptotes
    options['threshPC']       = .75    # Given in Percent correct on the unscaled sigmoid (reaching from 0 to 1)

    result = ps.psignifit(data,options)
    result['Fit']
    result['conf_Intervals']
    print(result['conf_Intervals'])

    # plot the figure with the psychometric function (don't forget the plt.show())
    result = ps.psignifit(data,options)
    slope = ps.getSlope(result, 1)
    print("Slope Weibull : " + str(slope))
    ps.psigniplot.plotPsych(result)

    plt.show()

#------------------------------------------------------ MAIN PART ------------------------------------------------------
def main_weibull(xl_path):
    # get the info from the excell file
    my_data_xls, my_dirname = catch_info_xls(xl_path) 
    # get the info from json file
    my_data_json = catch_info_json(my_dirname)
    number_trial = len(my_data_json)
    # dictionnary with all the info (hit, miss, GO timeout, false alarm, rejection)
    hfmr_dico = {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, "NOgo_false alarm" : 0, "NOgo_rejection" : 0, "NOgo_timeout_paw" : 0}


    ma_liste_freq_amp = liste_freq_amp(my_data_json)
    print(ma_liste_freq_amp)
    

    freq_dico_hit = {}
    freq_dico_miss = {}
    freq_dico_total_go = {}

    for icount_amp_liste in range (len(ma_liste_freq_amp)):
        freq_dico_hit[ma_liste_freq_amp[icount_amp_liste]] = 0
        freq_dico_miss[ma_liste_freq_amp[icount_amp_liste]] = 0
        freq_dico_total_go[ma_liste_freq_amp[icount_amp_liste]] = 0
    
    print(freq_dico_hit)

    liste_newtrial = search_nb_newtrial(my_data_xls, number_trial) # get the line  new trial
    liste_endtrial = search_nb_endtrial(my_data_xls, number_trial) # get the line of the end trial
    my_liste_diff = diff_new_end_trial(liste_newtrial, liste_endtrial) # get the range between new trial and end trial


    #loop to check all the information from the different trial
    for icount_liste_nbTrial in range (len(liste_newtrial)):
        #conditions => GO EVENT
        if my_data_json[icount_liste_nbTrial].get('trial_type') == "Go" :
            case_if_stim(hfmr_dico, my_liste_diff, my_data_xls, liste_newtrial, icount_liste_nbTrial,
            my_data_json, freq_dico_hit, freq_dico_miss, ma_liste_freq_amp)
        #conditions => NOGO event
        elif my_data_json[icount_liste_nbTrial].get('trial_type') == "Nogo" :
            case_if_NO_stim(hfmr_dico, my_liste_diff, my_data_xls, liste_newtrial, icount_liste_nbTrial)

    print(freq_dico_hit)

    #ad the value_hit + value_miss for all the different amplitude in total dictionnary 
    for (key1, value1), (key2, value2), (key3, value3) in zip (freq_dico_hit.items(), freq_dico_miss.items(), freq_dico_total_go.items()):
        valeur_total = value1 + value2 
        freq_dico_total_go[key3] = valeur_total

    print(freq_dico_total_go)

    hit_liste_rate = []
    for (key1, value1), (key2, value2) in zip (freq_dico_hit.items(), freq_dico_total_go.items()):
        hit_rate = value1 / value2
        hit_rate = float("{:.2f}".format(hit_rate))
        hit_liste_rate.append(hit_rate)
    
    print(hit_liste_rate)
    print(ma_liste_freq_amp)

    title_plot = get_title(my_data_xls)

    big_info = [freq_dico_hit, freq_dico_total_go, ma_liste_freq_amp, hit_liste_rate]

    save_myDico = True
    if save_myDico == True :
        save_eventDico_json(big_info, my_dirname)

    return hit_liste_rate, ma_liste_freq_amp, freq_dico_hit, freq_dico_total_go