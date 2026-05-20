"""
Alexandre CORNIER - 09/09/2021 - barplot.py
This code is part of the SpiFlash application as part of the work of Dr Ourania Semelidou on behaviors experiments.
This code allow us to know at the end the percentage of each event and the sensitivity.

This code allow us to get the number of Events (HIT, MISS, GO_TIMEOUT, FALSE ALARM, REJECTION, TIMEOUT PAW OFF).
At the end, we plot a bar plot of all the events
So, At the end we get a dictionary with all the information like this for example : {'GO_hit': 0, 'GO_miss': 0, 'GO_timeout': 1, 'NOgo_false alarm': 0, 'NOgo_rejection': 2, 'NOgo_timeout_paw': 2}
FIRST CONDITIONS (GO event): when there is a go stimuli we test if the mouse lick at the right time or before and the mouvement of the paw
SECOND CONDITIONS (NOGO event): when there is a nogo stimuli we test if the mouse try to lick (so it's a timeout Port1In) or if there is the mouvement of the before the stimuli (so it's a timeout BNC2Low).

EVENT :
if go + lick event => GO_hit
if go + no lick event = > GO_miss 
if go + timeout (paw off from the piezo or lick before stimuli) => GO_timeout

if Nogo + lick event => NOgo_false_alarm
if Nogo + no lick event => NOgo_rejection
if Nogo + Paw off the piezo => NOgo_timeout_paw

NUMBER(in the excel) :
94 => mouse break the beam so its corresponds to a Port1In, so TIMEOUT !
93 => mouse took his paw off from the piezo device before stimuli, so TIMEOUT !

This code is part of the SpiFlash a application as part of the work of Dr Ourania Semelidou on behaviors experiments.
This code allow us to know at the end the percentage of each event and the sensitivity.

"""

import json
import matplotlib.pyplot as plt
from scipy.stats import norm
from main_function_Sp import catch_info_xls, catch_info_json, search_nb_newtrial, search_nb_endtrial, diff_new_end_trial, case_if_stim, case_if_NO_stim, get_title

#------------------------------------------------------ SPECIFIC FUNCTION BARPLOT ------------------------------------------------------
#Save the dictionnary with all the event in a json format
def save_eventDico_json(the_dico,  directory_name):
    with open(str(directory_name) + '/infoBarplot.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)

'''
The sensitivity index is a dimensionless statistic used in signal detection theory. A higher index indicates that the signal can be more readily detected. 
To calculate this we need :
    - hit_rate = GO_hit / (GO_hit + GO_miss)
    - false alarm rate = NOgo_false_alarm / (Nogo_false_alarm + NOgo_rejection)

in the case of :
    - GO_hit + GO_miss = 0 or Nogo_false_alarm + NOgo_rejection = 0 , we are not available to calculate the sensitivity

then to obtain the sensitivity from hit rate and false alarm rate we have to calcutate the Z score for each with the norm.ppf
and at the end, we get the sensitivity by : s = Zscore(hit rate) - Zscore(false alarm rate)
the sensitivity results is print directly on SpiFlash app and in terminal too for copy/paste it
'''
def get_sensitivity (the_dico):
    # impossible to divide by 0 to do the hit rate 
    no_division = False
    if the_dico['GO_hit'] + the_dico['GO_miss'] == 0 or the_dico["NOgo_false alarm"] + the_dico["NOgo_rejection"] == 0 :
        no_division = True
        s = "Impossible division by zero (Go_hit = 0 or NOgo false alarm = 0)"

    if no_division == False :
        hit_rate = (the_dico['GO_hit'] / (the_dico['GO_hit'] + the_dico['GO_miss']))
        if hit_rate == 1:
            hit_rate = 0.99
        if hit_rate == 0:
            hit_rate = 0.01
            
        false_alarm_rate = (the_dico["NOgo_false alarm"] / (the_dico["NOgo_false alarm"] + the_dico["NOgo_rejection"]))
        if false_alarm_rate == 1:
            false_alarm_rate = 0.99
        if false_alarm_rate == 0:
            false_alarm_rate = 0.01

        print(hit_rate)
        print(false_alarm_rate)
        s = (norm.ppf(hit_rate)) - (norm.ppf(false_alarm_rate))
        s = float("{:.3f}".format(s))
        c = - (norm.ppf(hit_rate)) + (norm.ppf(false_alarm_rate)) / 2
        c = float("{:.3f}".format(c))

    dico_sensitivity = {"sensitivity" : s, "criterion" : c}

    sensitivity = "Sensitivity : " + str(s)
    return sensitivity, dico_sensitivity

#plotting part (barplot) using the Spiflash to show the results with a diagram
def plot_things(liste_x_names, liste_pourcent, my_title_plot, dir_name):

    print(liste_x_names)
    print(liste_pourcent)

    plt.rcParams.update({'font.size': 10})
    plt.rcParams["figure.figsize"] = (10,4)

    title_barplot = "Barplot " + str(my_title_plot)

    fig, axs = plt.subplots(1)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.set_ylim(0,100)
    axs.bar(liste_x_names, liste_pourcent)
    
    axs.legend(loc='best')
    axs.title.set_text(title_barplot)
    axs.set_xlabel('Events')
    axs.set_ylabel('%')

    plt.tight_layout()
    fig.savefig(str(dir_name) + "/barplot.svg", format = 'svg')
    plt.show()
    
#------------------------------------------------------ MAIN FUNCTION PART ------------------------------------------------------
def main_barplot(ma_path):
    # get the info from the excell file
    my_data_xls, my_dirname = catch_info_xls(ma_path) 
    # get the info from json file
    my_data_json = catch_info_json(my_dirname)
    number_trial = len(my_data_json)
    # dictionnary with all the info (hit, miss, GO timeout, false alarm, rejection)
    hfmr_dico = {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, "NOgo_false alarm" : 0, "NOgo_rejection" : 0, "NOgo_timeout_paw" : 0}

    liste_newtrial = search_nb_newtrial(my_data_xls, number_trial) # get the line  new trial
    liste_endtrial = search_nb_endtrial(my_data_xls, number_trial) # get the line of the end trial
    my_liste_diff = diff_new_end_trial(liste_newtrial, liste_endtrial) # get the range between new trial and end trial

    #loop to check all the information from the different trial
    for icount_liste_nbTrial in range (len(liste_newtrial)):
        print(my_data_json[icount_liste_nbTrial].get('trial_type'))
        if my_data_json[icount_liste_nbTrial].get('trial_type') == "Go" :
            case_if_stim(hfmr_dico, my_liste_diff, my_data_xls, liste_newtrial, icount_liste_nbTrial)
        elif my_data_json[icount_liste_nbTrial].get('trial_type') == "Nogo" :
            case_if_NO_stim(hfmr_dico, my_liste_diff, my_data_xls, liste_newtrial, icount_liste_nbTrial)

    print(hfmr_dico)
    print(len(liste_newtrial))
    
    x_names = []
    pourcent_x_values = []

    for key, values in hfmr_dico.items():
        x_names.append(key)
        final_results = (values * 100)/ len(liste_newtrial)
        final_results = float("{:.2f}".format(final_results))
        pourcent_x_values.append(final_results)
    
    title_plot = get_title(my_data_xls)

    my_sensitivity, sensitivity_dico = get_sensitivity(hfmr_dico)
    print(my_sensitivity)

    dico_info_barplot = [hfmr_dico, sensitivity_dico]

    save_eventDico_json(dico_info_barplot, my_dirname)

    return hfmr_dico, x_names, my_sensitivity, pourcent_x_values, title_plot, my_dirname
    
