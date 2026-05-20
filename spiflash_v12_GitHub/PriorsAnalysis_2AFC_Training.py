import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from psycho import save_eventDico_json as save_eventPsycho_json
from main_function_Sp import catch_info_xls, catch_info_json, search_nb_newtrial, search_nb_endtrial, \
    diff_new_end_trial, liste_freq_amp

""" (Adinda and Ourania)
This function returns return_info, which contains
1)
in the case of a previous right success trial, the probability of a
- HIT trial
- successful right lick trial
- Time out for right lick trial (so wrong classification as high amplitude = Low TO)
2)
in the case of a previous left success trial, the probability of a:
- HIT trial
- successful left trial
- Time out for left lick (so wrong classification as low amplitude = High TO)
4) the amount of trials following a right success and left success
 and the amount of these which are hits, successfull left or right lick trials and timeouts"""
ma_path =""
# Extract data from relevant files
my_data_xls, my_dirname = catch_info_xls(ma_path)
my_data_json = catch_info_json(my_dirname)
number_trial = len(my_data_json)

# get the line  new trial
liste_newtrial = search_nb_newtrial(my_data_xls, number_trial)
# get the line of the end trial
liste_endtrial = search_nb_endtrial(my_data_xls, number_trial)
# get the range between new trial and end trial
my_liste_diff = diff_new_end_trial(liste_newtrial, liste_endtrial)

'''Step 1: Identify success and time out trials for low and high amplitudes'''
# Initiate empty lists to store the success trials and  time out trials in for left and right
triallist_successleft = []
triallist_successright = []
triallist_to_left = []
triallist_to_right = []

# Identify the trial numbers of success & time out trials for left and right
for icount_liste_nbTrial in range(len(liste_newtrial)):
    print(icount_liste_nbTrial)
    for i in range(my_liste_diff[icount_liste_nbTrial]):
        if my_data_xls.iloc[liste_newtrial[icount_liste_nbTrial]][4] == "Reward_left":
            triallist_successleft.append(icount_liste_nbTrial)
            break
        elif my_data_xls.iloc[liste_newtrial[icount_liste_nbTrial]][4] == "Reward_right":
            triallist_successright.append(icount_liste_nbTrial)
            break
        elif my_data_xls.iloc[liste_newtrial[icount_liste_nbTrial]][4] == "Timeout":
            # Check whether this trial was high or low amplitude trial
            if my_data_json[icount_liste_nbTrial].get('trial_type') == "high":
                triallist_to_right.append(icount_liste_nbTrial)
                break
            else:
                triallist_to_left.append(icount_liste_nbTrial)
                break
        # if the conditions are not good we will go the next line
        else:
            liste_newtrial[icount_liste_nbTrial] += 1
            i += 1
'''Step 2: get the number of HIT trials, successful right lick trials, time out trials following the previously
identified trials'''
# Set counters at 0
prior_rightsuccess_dico_ = {"Hit after right": 0, "Hit right after right": 0, "Timeout left after right": 0}
prior_leftsuccess_dico = {"Hit after left": 0, "Hit left after left": 0, "Timeout right after left": 0}

# For the trials following a right success trial
for identified_rightsuccess in range(len(triallist_successright)):
    nexttrial = triallist_successright[identified_rightsuccess] + 1
    if nexttrial in triallist_successright:
        prior_rightsuccess_dico_["Hit after right"] += 1
        prior_rightsuccess_dico_["Hit right after right"] += 1
    elif nexttrial in triallist_successleft:
        prior_rightsuccess_dico_["Hit after right"] += 1
    elif nexttrial in triallist_to_left:
        prior_rightsuccess_dico_["Timeout left after right"] += 1
print(triallist_successleft)
# Same but for trials following a low success trial
for identified_leftsuccess in range(len(triallist_successleft)):

    nexttrial = triallist_successleft[identified_leftsuccess] + 1
    if nexttrial in triallist_successleft:
        prior_leftsuccess_dico["Hit after left"] += 1
        prior_leftsuccess_dico["Hit left after left"] += 1
    elif nexttrial in triallist_successright:
        prior_leftsuccess_dico["Hit after left"] += 1
    elif nexttrial in triallist_to_right:
        prior_leftsuccess_dico["Timeout right after left"] += 1

'''Step 3: calculate the frequencies'''
# First identify the number of trials following a high success trial:
    # Check if the last trial that is in the list of successful trials is also the last trial of the session
if number_trial == triallist_successright[-1]:
    # if yes, then the number of trials following a right success = the number of right success trials - 1
    trials_following_rightsuccess = len(triallist_successright) - 1
else:
    # if no, then the number of trials following a right success = the number of right success trials
    trials_following_rightsuccess = len(triallist_successright)
# Same for the frequency of trialtypes following a left success trial
if triallist_successleft[-1] == number_trial:
    trials_following_leftsuccess = len(triallist_successleft) - 1
else:
    trials_following_leftsuccess = len(triallist_successleft)
trials_following_successes = {"Trials after right success": trials_following_rightsuccess,
                              "Trials after left success": trials_following_leftsuccess}
# Calculate the frequencies
# First for trials following right success trials
freq_after_rightsuccesslist = []
after_rightsuccess_names = ["Freq hit after right success", "Freq hit right after right successs",
                            "Freq timeout left after right success"]
for key, values in prior_rightsuccess_dico_.items():
    final_frequencies_right = values / trials_following_rightsuccess
    final_frequencies_right = float("{:.2f}".format(final_frequencies_right))
    freq_after_rightsuccesslist.append(final_frequencies_right)
freq_after_rightsuccess = {i: j for i, j in zip(after_rightsuccess_names, freq_after_rightsuccesslist)}
# Same but for trials following left success trials
freq_after_leftsuccesslist = []
after_leftsuccess_names = ["Freq hit after left success", "Freq hit left after left success",
                           "Freq timeout right after left success"]
for key, values in prior_leftsuccess_dico.items():
    final_frequencies_left = values / trials_following_leftsuccess
    final_frequencies_left = float("{:.2f}".format(final_frequencies_left))
    freq_after_leftsuccesslist.append(final_frequencies_left)
freq_after_leftsuccess = {i: j for i, j in zip(after_leftsuccess_names, freq_after_leftsuccesslist)}


return_info = [freq_after_rightsuccess, freq_after_leftsuccess, prior_rightsuccess_dico_, prior_leftsuccess_dico,
               trials_following_successes]

with open(str(my_dirname) + '/infoPriors.json', 'w') as jsonFile:
    json.dump(return_info, jsonFile, indent=4)