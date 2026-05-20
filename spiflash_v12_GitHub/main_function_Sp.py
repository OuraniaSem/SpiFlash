import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import ast
from scipy.stats import norm

#return the info from excell file, and the path of the directory name 
def catch_info_xls(la_file):
    dirname, basename = os.path.split(la_file) #basename we don't care it's just to split the path to just get the folder (dirname)
    read_file = pd.read_excel(la_file ,header=None)
    
    return read_file, dirname

#return the info from the json with all informations about the frenquencies and amplitude file
#from the the same folder as the directory name get by the catch_info_xls function
def catch_info_json(directory_name):
    myFile_json = str(directory_name) + "/params_trial.json"
    with open(myFile_json, "r") as read_file:
        info_json = json.load(read_file)

    return info_json

#return a list of the position of different trial in the excel file (the lines where is the string "New trial")
#so at the end, list_index_newtrial is a list with all the position of each "New trial" in the excel file
def search_nb_newtrial(data, nb_trial):
    list_index_newtrial = []

    for i in range (nb_trial): #pick the number of trial
        my_index = data[data[4] == 'New trial'].index[i]
        list_index_newtrial.append(my_index)

    return list_index_newtrial

#return index of all the end trial in the columm E of the excell file (the lines where is the string "The Trial ended")
#so at the end, list_index_endtrial is a list with all the position of each "The Trial ended" in the excel file
def search_nb_endtrial(data, nb_trial):
    list_index_endtrial = []

    for i in range (nb_trial):
        my_index = data[data[4] == 'The trial ended'].index[i]
        list_index_endtrial.append(my_index)

    return list_index_endtrial

#here we want for each trial, the numbers of lines between "New trial" and "The trial ended" in order to navigate and obtain information on events
# at the end, liste_diff_newEndTrial return a liste of numbers of lines for each event
def diff_new_end_trial(where_newtrial, where_endtrial):
    liste_diff_newEndTrial = []

    for icount_liste in range (len(where_newtrial)):
        diff = where_endtrial[icount_liste] - where_newtrial[icount_liste]
        liste_diff_newEndTrial.append(diff)
    
    return liste_diff_newEndTrial

'''
This function allow us to count the number of GO_events (GO_hit, GO_miss & GO_timeout), so when there is stimulation during the experiments
REQUIREMENTS :
    - We need a dictionary that is initialize in the main function : {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, "NOgo_false alarm" : 0, "NOgo_rejection" : 0, "NOgo_timeout_paw" : 0}
    - Then the list with the differences between new and end trial
    - Information from the excel file
    - The list of the new trial to know where to start to navigate inside the excel file (specific lines)
    - And finally a counter initialize in the loop in the main function
RETURN : 
    - At the end, this function return the dictionary with the different event identified (GO_hit, GO_miss, GO_timeout)
    this function is only used in the case of a GO type event. This condition is checked in the main function using the json file

'''
def case_if_stim(the_dico, the_liste_diff, data_xls, the_liste_newTrial, counteur):
    my_hit = False
    my_timeout = False
    for i in range (the_liste_diff[counteur]):
        #print the currently line
        print(data_xls.iloc[the_liste_newTrial[counteur]][4])

        if data_xls.iloc[the_liste_newTrial[counteur]][4] == "Reward" :
            print("It's a HIT !")
            my_hit = True
            the_dico["GO_hit"] += 1
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
    
    
    print('TRIAL NUMBER : ', counteur)
    print (the_dico)
    print('\n')
    return the_dico

'''
This function allow us to count the number of NOgo_events (NOgo_false_alarm, NOgo_rejection & NOgo_timeout_paw), so when there is NO stimulation during the experiments
REQUIREMENTS :
    - We need a dictionary that is initialized in the main function : {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, "NOgo_false alarm" : 0, "NOgo_rejection" : 0, "NOgo_timeout_paw" : 0}
    - Then the list with the differences between new and end trial
    - Information from the excel file
    - The list of the new trial to know where to start to navigate inside the excel file (specific lines)
    - And finally a counter initialize in the loop in the main function
RETURN : 
    - At the end, this function return the dictionary with the different event identified (NOgo_false_alarm, NOgo_rejection & NOgo_timeout_paw)
    this function is only used in the case of a NO go type event. This condition is checked in the main function using the json file

'''
def case_if_NO_stim(the_dico, the_liste_diff, data_xls, the_liste_newTrial, counteur):
    my_false_alarm = False
    my_timeout_pawoff = False
    for i in range (the_liste_diff[counteur]):
        #print the current line in the excell file between new trial and end trial
        print(data_xls.iloc[the_liste_newTrial[counteur]][4])

        if data_xls.iloc[the_liste_newTrial[counteur]][4] == "Timeout" :
            print("there is a timeout (NOGO)!")
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
        print("there is a rejection (NOGO)!")
        the_dico["NOgo_rejection"] += 1
    
    print('TRIAL NUMBER : ', counteur + 1)
    print (the_dico)
    print('\n')
    return the_dico

#Allow us tho get back automatically the subject name of the mouse to use it as the title for the plotting part
def get_title(data_xls):
    my_index = data_xls[data_xls[4] == 'SUBJECT-NAME']
    my_title = ast.literal_eval(my_index.values[0][5])
    my_final_title = my_title[0]
    return my_final_title

#return an order list for the frequency and values amplitude 
def liste_freq_amp(info_json):
    my_liste_freq = []
    my_liste_amp = []
    for icount_json in range (len(info_json)):
        my_liste_freq.append(info_json[icount_json].get("freq"))
        my_liste_amp.append(info_json[icount_json].get("amp"))
    
    order_liste_freq = list(set(my_liste_freq))
    order_liste_freq.sort()
    if order_liste_freq[0] == 0:
        order_liste_freq.remove(0)

    order_liste_amp = list(set(my_liste_amp))
    order_liste_amp.sort()
    if order_liste_amp[0] == 0:
        order_liste_amp.remove(0)

    if len(order_liste_freq) > 1 :
        return order_liste_freq
    
    else :
        return order_liste_amp