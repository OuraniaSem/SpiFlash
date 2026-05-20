import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, fsolve
from psycho import save_eventDico_json as save_eventPsycho_json
from main_function_Sp import catch_info_xls, catch_info_json, search_nb_newtrial, search_nb_endtrial, \
    diff_new_end_trial, liste_freq_amp

def find_x_for_y_0_5(x, x0, k):
    return(sigmoid(x, x0, k)) - 0.5

def save_barplot_json(the_dico, directory_name):
    with open(str(directory_name) + '/infoBarplot.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)

def save_eventdico_json(the_dico, directory_name):
    with open(str(directory_name) + '/data_event_full.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)

def catch_info_data_event_full(directory_name):
    myfile_json = str(directory_name) + "/data_event_full.json"
    with open(myfile_json, "r") as read_file:
        info_json = json.load(read_file)

    return info_json

def barplot_2afc(ma_path):
    my_data_xls, my_dirname = catch_info_xls(ma_path)
    my_data_json = catch_info_json(my_dirname)
    number_trial = len(my_data_json)

    two_afc_dico = {"Reward Low": 0, "Reward High": 0,
                    "Miss Low": 0, "Miss High": 0,
                    "Timeout Low": 0, "Timeout High": 0}
    liste_newtrial = search_nb_newtrial(my_data_xls, number_trial)  # get the line  new trial
    liste_endtrial = search_nb_endtrial(my_data_xls, number_trial)  # get the line of the end trial
    my_liste_diff = diff_new_end_trial(liste_newtrial, liste_endtrial)  # get the range between new trial and end trial

    triallist_successleft = []
    triallist_successright = []

    for icount_liste_nbTrial in range(len(liste_newtrial)):
        my_hit = False
        my_timeout = False
        for i in range(my_liste_diff[icount_liste_nbTrial]):

            if my_data_xls.iloc[liste_newtrial[icount_liste_nbTrial]][4] == "Reward_left":
                my_hit = True
                two_afc_dico["Reward Low"] += 1
                triallist_successleft.append(icount_liste_nbTrial)
                break

            elif my_data_xls.iloc[liste_newtrial[icount_liste_nbTrial]][4] == "Reward_right":
                my_hit = True
                two_afc_dico["Reward High"] += 1
                triallist_successright.append(icount_liste_nbTrial)
                break

            elif my_data_xls.iloc[liste_newtrial[icount_liste_nbTrial]][4] == "Timeout":
                my_timeout = True
                # Check whether this trial was high or low amplitude trial
                if my_data_json[icount_liste_nbTrial].get('trial_type') == "high":
                    two_afc_dico["Timeout High"] += 1
                else:
                    two_afc_dico["Timeout Low"] += 1
                break

            # if the conditions are not good we will go the next line
            else:
                liste_newtrial[icount_liste_nbTrial] += 1
                i += 1

        # in case in all the trial there is no reward event or timeout event,
        # it's a miss because there is a stimuli but not action from the mouse
        if my_hit is False and my_timeout is False:
            # Check whether this was high or low amplitude trial
            if my_data_json[icount_liste_nbTrial].get('trial_type') == "high":
                two_afc_dico["Miss High"] += 1
            else:
                two_afc_dico["Miss Low"] += 1
    x_names = []
    pourcent_x_values = []

    for key, values in two_afc_dico.items():
        x_names.append(key)
        final_results = (values * 100) / len(liste_newtrial)
        final_results = float("{:.2f}".format(final_results))
        pourcent_x_values.append(final_results)
    save_barplot_json([two_afc_dico], my_dirname)

    plt.rcParams.update({'font.size': 10})
    plt.rcParams["figure.figsize"] = (10, 4)

    title_barplot = "Barplot 2AFC"

    fig, axs = plt.subplots(1)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.set_ylim(0, 100)
    axs.bar(x_names, pourcent_x_values, color="cyan")

    axs.legend(loc='best')
    axs.title.set_text(title_barplot)
    axs.set_xlabel('Events')
    axs.set_ylabel('%')

    plt.tight_layout()
    fig.savefig(str(my_dirname) + "/barplot_2AFC.svg", format='svg')
    plt.show()

def training_2afc(ma_path):
    """Original code by Alex, adapted by Adinda:
    Returns
    - trace of the training (percentage of hits and timeouts per 10 trials throughout the session
    - data_event_full: json file with number of HITS, Timeouts and Misses, seperated per trial type (left/right)
    per 10 trials
    """
    my_data_xls, my_dirname = catch_info_xls(ma_path)
    my_data_json = catch_info_json(my_dirname)
    number_trial = len(my_data_json)

    two_afc_dico = {"Reward": 0, "Miss": 0, "Timeout": 0}
    # Make separate dico to store data event full (necessary for wrap)
    two_afc_dico_def = {"Reward Left": 0, "Reward Right": 0,
                        "Miss Left": 0, "Miss Right": 0,
                        "Timeout Left": 0, "Timeout Right": 0}
    liste_newtrial = search_nb_newtrial(my_data_xls, number_trial)  # get the line  new trial
    liste_endtrial = search_nb_endtrial(my_data_xls, number_trial)  # get the line of the end trial
    my_liste_diff = diff_new_end_trial(liste_newtrial, liste_endtrial)  # get the range between new trial and end trial

    liste_hfmr = []
    liste_total_trial = []

    # use this as a counter for the global list
    about_trial_20 = 0

    for icount_liste_nbtrial in range(len(liste_newtrial)):
        my_hit = False
        my_timeout = False
        about_trial_20 += 1
        for i in range(my_liste_diff[icount_liste_nbtrial]):
            if my_data_xls.iloc[liste_newtrial[icount_liste_nbtrial]][4] == "Reward_left":
                my_hit = True
                two_afc_dico["Reward"] += 1
                two_afc_dico_def["Reward Left"] += 1
                break

            elif my_data_xls.iloc[liste_newtrial[icount_liste_nbtrial]][4] == "Reward_right":
                my_hit = True
                two_afc_dico["Reward"] += 1
                two_afc_dico_def["Reward Right"] += 1
                break

            elif my_data_xls.iloc[liste_newtrial[icount_liste_nbtrial]][4] == "Timeout":
                my_timeout = True
                two_afc_dico["Timeout"] += 1
                # Check whether this trial was high or low amplitude trial
                if my_data_json[icount_liste_nbtrial].get('trial_type') == "high":
                    two_afc_dico_def["Timeout Right"] += 1
                else:
                    two_afc_dico_def["Timeout Left"] += 1
                break

            # if the conditions are not good we will go the next line
            else:
                liste_newtrial[icount_liste_nbtrial] += 1
                i += 1

        # in case in all the trial there is no reward event or timeout event,
        # it's a miss because there is a stimuli but not action from the mouse
        if my_hit is False and my_timeout is False:
            two_afc_dico["Miss"] += 1
            # Check whether this was high or low amplitude trial
            if my_data_json[icount_liste_nbtrial].get('trial_type') == "high":
                two_afc_dico_def["Miss Right"] += 1
            else:
                two_afc_dico_def["Miss Left"] += 1
        count = 1
        if about_trial_20 == 10:
            count += 1
            liste_hfmr.append(two_afc_dico_def)
            wait_trial_total = two_afc_dico_def["Reward Right"] + two_afc_dico_def["Reward Left"] \
                               + two_afc_dico_def["Timeout Right"] + two_afc_dico_def["Timeout Left"] \
                               + two_afc_dico_def["Miss Right"] + two_afc_dico_def["Miss Left"]

            liste_total_trial.append(wait_trial_total)
            two_afc_dico_def = {"Reward Right": 0, "Reward Left": 0,
                                "Timeout Right": 0, "Timeout Left": 0,
                                "Miss Right": 0, "Miss Left": 0}
            about_trial_20 = 0

    # Safe information on trials as well as the number of trials in the session (important for priors analysis)
    save_eventdico_json(liste_hfmr, my_dirname)
    data_event = catch_info_data_event_full(my_dirname)

    liste_x_names = []
    for i in range(0, len(liste_newtrial), 10):
        i += 10
        liste_x_names.append(i)

    x_names = np.array(liste_x_names)

    liste_x_values = []
    pourcent_x_values_reward = []
    pourcent_x_values_timeout = []

    for icount_liste in range(len(data_event)):
        x_values1 = data_event[icount_liste]["Reward Right"]
        x_values2 = data_event[icount_liste]["Reward Left"]
        x_values = x_values1 + x_values2
        liste_x_values.append(x_values)
        final_results = (x_values * 100) / liste_total_trial[icount_liste]
        final_results = float("{:.2f}".format(final_results))
        pourcent_x_values_reward.append(final_results)

    for icount_liste in range(len(data_event)):
        x_values1 = data_event[icount_liste]["Timeout Right"]
        x_values2 = data_event[icount_liste]["Timeout Left"]
        x_values = x_values1 + x_values2
        liste_x_values.append(x_values)
        final_results = (x_values * 100) / liste_total_trial[icount_liste]
        final_results = float("{:.2f}".format(final_results))
        pourcent_x_values_timeout.append(final_results)

    linear_model_hit = np.polyfit(x_names, pourcent_x_values_reward, 2)
    linear_model_fn_hit = np.poly1d(linear_model_hit)
    linear_model_timeout = np.polyfit(x_names, pourcent_x_values_timeout, 2)
    linear_model_fn_timeout = np.poly1d(linear_model_timeout)
    x_s = np.arange(0, x_names[-1])

    plt.rcParams.update({'font.size': 16})
    plt.rcParams["figure.figsize"] = (8, 6)

    title_hit = 'Training trace Reward 2AFC '
    title_timeout = 'Training trace Timeout 2AFC '

    fig, axs = plt.subplots(2)

    axs[0].plot(x_names, pourcent_x_values_reward, "o", color="blue", label="Reward")
    axs[0].plot(x_s, linear_model_fn_hit(x_s), color="cyan", label="Fit Reward")

    axs[1].plot(x_names, pourcent_x_values_timeout, "o", color="orange", label="Timeout")
    axs[1].plot(x_s, linear_model_fn_timeout(x_s), color="red", label="Fit Timeout")

    axs[0].title.set_text(title_hit)
    axs[0].set_xlabel('Number of trials')
    axs[0].set_ylabel('Hit (%)')
    axs[1].title.set_text(title_timeout)
    axs[1].set_xlabel('Number of trials')
    axs[1].set_ylabel('Timeout (%)')

    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)

    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    axs[0].set_ylim([0, 100])
    axs[1].set_ylim([0, 100])

    plt.tight_layout()
    fig.savefig(str(my_dirname) + "/TrainingTrace.svg")
    plt.show()

# Sigmoid function
def sigmoid(x, x0, k):
    y = 1 / (1 + np.exp(-k * (x - x0)))
    return y

def psycho_2afc(xl_path):
    """ (Adinda)
    Returns and saves psychometric curve plot and infoPsychoJson file
    Psychometric curve shows the amount of trials where the mouse licked rightwards (y-axis)
    for each stimulus amplitude (x-axis).
    For this purpose we identify for each stimulus amplitude:
    - the total number of trials that had a stimulus of this amplitude
    - the number of trials with this stimulus amplitude that the mouse responded to with a rightwards lick
    infoPsychoJson file stores:
        - # rightward trials per amplitude
        - # leftward trials per amplitude
        - # missed trials per amplitude
        - # total trials that were given for each amplitude
        - List of the amplitudes that were given
        - The frequency of rightward trials for each amplitude (over all trials in which this amplitude was given)
        - The frequency of leftward trials for each amplitude
        - The frequency of miss trials for each amplitude """
    # get the info from the excell file
    xls_data, my_dirname = catch_info_xls(xl_path)
    # get the info from json file
    my_data_json = catch_info_json(my_dirname)
    """    Step 1: Extract relevant data from relevant files
    We differentiate between two types of trials:
    1) Trials that the mouse identified as high amplitude stimulus, licking rightwards
    2) Trials that were not identified as high amplitude stimulus (licking leftwards or not licking at all)
    We want to only take into account the direction of the first lick in the response window
    We obtain a matrix Stim_response with size = NumberOfTrials x 2: 
    - column 1: the stimulus amplitude of a trial,
    - column 2: whether the mouse licked right first during the response window 
        (indicated by a 1 instead of a 0 or 2)"""
    # Find the number of trials
    number_of_trials = len(my_data_json)
    # Get the line number for the beginning and ending of each trial
    start_trials = search_nb_newtrial(xls_data, number_of_trials)
    end_trials = search_nb_endtrial(xls_data, number_of_trials)
    # Get number of lines between the start & end of each trial
    start_to_end_trials = diff_new_end_trial(start_trials, end_trials)
    # Make array to store for each trial the stimulus amplitude in the first column,
    # And in the 2nd column a 1 for right licks, 2 for left licks following the stimulus and 0 if there was no response
    stim_response = np.zeros((number_of_trials, 2))
    # For each trial identify the stimulus amplitude and if the mouse chose to lick rightwards
    for counter_trials in range(number_of_trials):
        # Store the stimulus amplitude for each trial and put in array
        stimulus_amplitude = my_data_json[counter_trials].get('amp')
        stim_response[counter_trials, 0] = stimulus_amplitude
        # Find the start of the response window for this trial
        for within_trials in range(start_to_end_trials[counter_trials]):
            position1 = start_trials[counter_trials] + within_trials
            if xls_data.iloc[position1][4] == 'ResponseWindow' and xls_data.iloc[position1][0] == 'TRANSITION':
                rw_position = position1
        # Find out whether the first lick in the responseWindow is rightwards or not
        # From the start of the response window until the end of the trial
        while not (rw_position == end_trials[counter_trials]):
            # Check if the first recorded lick was rightwards
            if xls_data.iloc[rw_position][4] == 94:
                # Indicate that this trial was identified as high amplitude stimulus by mouse
                stim_response[counter_trials, 1] = 1
                # if this is the case, finish here
                rw_position = end_trials[counter_trials]
            # Check whether the first recorded lick was leftwards
            elif xls_data.iloc[rw_position][4] == 96:
                # Indicate that this trial was identified as low amplitude stimulus by mouse
                stim_response[counter_trials, 1] = 2
                # if this is the case, finish here
                rw_position = end_trials[counter_trials]
            else:
                # In this case this position in the Excel file does not contain info on licks, so we go to the next line
                rw_position += 1
    amplitude_list = liste_freq_amp(my_data_json)

    # Since we want to make a file saving the amount of right, left and miss trials for each stimulus,
    # We should initiate these at 0
    freq_dico_r = {}
    freq_dico_miss = {}
    freq_dico_l = {}
    # Same for the number of trials for each stimulus
    freq_dico_total_go = {}
    total_trials_amp = {}

    for icount_amp_liste in range(len(amplitude_list)):
        freq_dico_r[amplitude_list[icount_amp_liste]] = 0
        freq_dico_miss[amplitude_list[icount_amp_liste]] = 0
        freq_dico_l[amplitude_list[icount_amp_liste]] = 0
        freq_dico_total_go[amplitude_list[icount_amp_liste]] = 0
        total_trials_amp[amplitude_list[icount_amp_liste]] = 0

    '''Step 2: Get frequency of 'Right lick' trials for each stimulus amplitude
    Obtains a matrix with in column 1 the amplitude, and column 2 the frequency of right trials'''
    number_of_amplitudes = len(amplitude_list)
    # Obtain frequency of right trials
    for i in range(len(amplitude_list)):
        find_amplitude = amplitude_list[i]
        # Count the number of trials in which this stimulus amplitude was given
        count_amp_trials = np.count_nonzero(stim_response[:, 0] == find_amplitude)
        # Add this to the dictionary of the total trials that were given for each amplitude
        total_trials_amp[find_amplitude] = count_amp_trials
        # Find the number of trials in which this stimulus amplitude was given and the mouse licked rightwards
        for j in range(number_of_trials):
            # In trials of this stimulus amplitude where the response was rightwards,
            # add 1 to the counter of right trials
            if stim_response[j, 0] == find_amplitude and stim_response[j, 1] == 1:
                freq_dico_r[find_amplitude] += 1
            # Also find number of miss and left-lick trials per amplitude
            if stim_response[j, 0] == find_amplitude and stim_response[j, 1] == 2:
                freq_dico_l[find_amplitude] += 1
            if stim_response[j, 0] == find_amplitude and stim_response[j, 1] == 0:
                freq_dico_miss[find_amplitude] += 1
    '''Calculate frequency types of trials from trials with this stimulus amplitude'''
    freq_right = {k: freq_dico_r[k] / float(total_trials_amp[k]) for k in total_trials_amp if k in freq_dico_r}
    freq_left = {k: freq_dico_l[k] / float(total_trials_amp[k]) for k in total_trials_amp if k in freq_dico_l}
    freq_miss = {k: freq_dico_miss[k] / float(total_trials_amp[k]) for k in total_trials_amp if k in freq_dico_miss}

    '''Step 3: Plot data'''
    xdata = list(freq_right.keys())
    ydata = list(freq_right.values())
    plt.plot(xdata, ydata, 'k.', label='data')
    plt.ylim(0, 1)
    plt.xlabel('Amplitude of stimulus')
    plt.ylabel('Frequency of rightward lick response trials')
    plt.title('Psychometric curve')
    dico_psycho = {"Slope": 0, "Discrimination threshold": 0}
    if number_of_amplitudes >= 3:
        popt, pcov = curve_fit(sigmoid, xdata, ydata, maxfev=3000)
        fix_value = amplitude_list[-1] + 0.1
        x = np.linspace(0, fix_value, 500)
        y = sigmoid(x, *popt)
        plt.plot(x, y, label='fit')
        xmax = amplitude_list[-1] + 0.12
        plt.xlim(1, xmax)

        # Find the y-value for which X = 0.5 to determine the discrimination threshold
        x_for_y_0_5 = fsolve(find_x_for_y_0_5, x0=0, args=(popt[0], popt[1]))
        x_for_y_0_5 = x_for_y_0_5.tolist()[0]
        print(x_for_y_0_5)

        # Extract slope
        slope, intercept = np.polyfit(x, y, 1)
        dico_psycho = {"Slope": slope, "Discrimination threshold": x_for_y_0_5}
        print("slope np: " + str(slope))

    plt.show()
    plt.savefig(str(my_dirname) + "/PsychometricCurve")
    # Save info psycho
    big_info = [dico_psycho, freq_dico_r, freq_dico_l, freq_dico_miss, total_trials_amp, amplitude_list, freq_right, freq_left,
                freq_miss]
    save_eventPsycho_json(big_info, my_dirname)

def heatmap_2afc(xl_path):
    """ (Adinda)
    Function to obtain a heat map of the timepoints at which the mouse licks over different trials for the 2AFC task:
    Y-axis: trials, X-axis: time relative to stimulus delivery per trial
    Three different figures are plotted and saved:
    1 with the trials in which the mouse correctly responded to the stimulus
    1 with the trials that had high amplitude stimuli & incorrect (leftwards) responses resulting in time out.
    1 with the trials that had low amplitude stimuli & incorrect (rightwards) responses resulting in time out

    Note: In time-out trials I was unable to put the legend in a way that it correctly differentiates
    between the left and right licks. Now it shows wrong-side-licks in red & right-side-licks in black,
    hopefully this is sufficiently intuitive to read"""
    # get the info from the excell file
    xls_data, my_dirname = catch_info_xls(xl_path)
    # get the info from json file
    my_data_json = catch_info_json(my_dirname)
    number_of_trials = len(my_data_json)
    '''Step 1 consists of extracting all the necessary info from our Excel and json file.
    We wish to identify the timing of each lick per trial, as well as the timing the stimulus was given in each trial
    These variables will be stored in LicksPerTrial and Stimulus_timing respectively'''
    # Get the line number for the beginning and ending of each trial
    start_trials = search_nb_newtrial(xls_data, number_of_trials)
    end_trials = search_nb_endtrial(xls_data, number_of_trials)
    # Get number of lines between the start & end of each trial
    start_to_end_trials = diff_new_end_trial(start_trials, end_trials)

    # Get the max number of licks in a trial: Identify the licks in time for each trial
    number_licks_trial = []  # Make an empty array to store the number of licks for each trial
    for counter_trials in range(number_of_trials):  # For every trial
        counter_licks = 0  # Set counter to 0
        for within_trials in range(
                start_to_end_trials[counter_trials]):  # Looping over every line corresponding to said trial
            # Find the position of the line we want to look for info in the excell file
            position = start_trials[counter_trials] + within_trials
            # 94 means the red laser beam was interrupted, corresponding to a lick event of the mouse
            if xls_data.iloc[position][4] == 94 or xls_data.iloc[position][4] == 96:
                counter_licks += 1
        number_licks_trial.append(counter_licks)
    max_licks_trial = max(number_licks_trial)
    # Make empty array to put the stimulus time in for each trial (again each row will represent a trial)
    stimulus_timing = np.zeros((number_of_trials, 1))  # zeroes because some trials never get stimulus after time-outs!
    trial_type = np.empty(number_of_trials)
    trial_type = trial_type.tolist()
    high_success_trials = []
    low_success_trials = []
    high_to_trials = []
    low_to_trials = []
    high_miss_trials = []
    low_miss_trials = []
    '''Step 1.a: identify between
    - High amplitude stimulus trials: successful vs unsuccessful 
    - Low amplitude stimulus trials: successful vs unsuccessful'''
    for counter_trials in range(number_of_trials):  # For every trial
        # Obtain the time at which the stimulus was given for each trial
        missed_trial = True
        for within_trials in range(start_to_end_trials[counter_trials]):
            # Identify the position of the line we want to look for info in the excell file
            position = start_trials[counter_trials] + within_trials
            # Add to Stimulus_timing matrix
            if xls_data.iloc[position][4] == 'Stimulus' and xls_data.iloc[position][0] == 'TRANSITION':
                timing = xls_data.iloc[position][2]
                stimulus_timing[counter_trials, 0] = timing
            # Identify the type of stimulus that was given and append to right list
            # For high amplitude stimulus trials
            if my_data_json[counter_trials].get('trial_type') == "high":
                # Identify whether the trial was successful or not
                if xls_data.iloc[position][4] == 'Reward_right' and xls_data.iloc[position][0] == 'TRANSITION':
                    high_success_trials.append(counter_trials)
                    trial_type[counter_trials] = 'HighSuccess'
                if xls_data.iloc[position][4] == 'Timeout' and xls_data.iloc[position][0] == 'TRANSITION':
                    high_to_trials.append(counter_trials)
                    trial_type[counter_trials] = 'HighTO'
            # For low amplitude stimulus trials
            if my_data_json[counter_trials].get('trial_type') == "low":
                if xls_data.iloc[position][4] == 'Reward_left' and xls_data.iloc[position][0] == 'TRANSITION':
                    low_success_trials.append(counter_trials)
                    trial_type[counter_trials] = 'LowSuccess'
                if xls_data.iloc[position][4] == 'Timeout' and xls_data.iloc[position][0] == 'TRANSITION':
                    low_to_trials.append(counter_trials)
                    trial_type[counter_trials] = 'LowTO'

    '''Step 1.b Identify the lick times for each trial and add to corresponding matrix.
    We store left and right lick time points in different matrices for Time Out trials only, 
    since in successful trials the direction of licks can be assumed based on the trial type
    '''
    # Make empty matrices to put lick times in for each trial,
    # depending on the trial type and the success of the trial
    licks_high_success = np.empty((number_of_trials, max_licks_trial))
    licks_high_success[:] = np.NaN
    licks_r_high_to = np.empty((number_of_trials, max_licks_trial))
    licks_r_high_to[:] = np.NaN
    licks_l_high_to = np.empty((number_of_trials, max_licks_trial))
    licks_l_high_to[:] = np.NaN
    licks_low_success = np.empty((number_of_trials, max_licks_trial))
    licks_low_success[:] = np.NaN
    licks_r_low_to = np.empty((number_of_trials, max_licks_trial))
    licks_r_low_to[:] = np.NaN
    licks_l_low_to = np.empty((number_of_trials, max_licks_trial))
    licks_l_low_to[:] = np.NaN

    for trial in range(number_of_trials):  # For every trial
        # Set counter for each category of trial to 0
        count_high_success = 0
        count_r_high_to = 0
        count_l_high_to = 0
        count_low_success = 0
        count_r_low_to = 0
        count_l_low_to = 0
        # Every line corresponding to trial
        for within_trials in range(start_to_end_trials[trial]):
            # Identify the position of the line we want to look for info in the Excel file
            position = start_trials[trial] + within_trials
            # Check if there was a lick in this line
            if xls_data.iloc[position][4] == 94 or xls_data.iloc[position][4] == 96:
                # Find the corresponding time in column C of the Excel file
                time_lick = xls_data.iloc[position][2]
                # Check in which matrix the time value should be added
                # For trials with high stimulus & successful response
                if trial_type[trial] == "HighSuccess":
                    licks_high_success[trial, count_high_success] = time_lick
                    count_high_success += 1
                # For trials with low stimulus & successful response
                elif trial_type[trial] == "LowSuccess":
                    licks_low_success[trial, count_low_success] = time_lick
                    count_low_success += 1
                # For trials with high stimulus & TO
                elif trial_type[trial] == "HighTO":
                    # Check whether lick was left or right sided
                    if xls_data.iloc[position][4] == 94:  # Lick was rightwards
                        licks_r_high_to[trial, count_r_high_to] = time_lick
                        count_r_high_to += 1
                    # Lick was leftwards
                    else:
                        licks_l_high_to[trial, count_l_high_to] = time_lick
                        count_l_high_to += 1
                # For trials with low stimulus & TO
                elif trial_type[trial] == "LowTO":
                    # Rightward lick
                    if xls_data.iloc[position][4] == 94:
                        licks_r_low_to[trial, count_r_low_to] = time_lick
                        count_r_low_to += 1
                    # Lick was leftwards
                    else:
                        licks_l_low_to[trial, count_l_low_to] = time_lick
                        count_l_low_to += 1

    ''' Step 2: Transform lick time data relative to Stimulus_timing data, 
    so that stimulus delivery time t= 0 for every trial'''
    trans_high_success = licks_high_success - stimulus_timing
    trans_low_success = licks_low_success - stimulus_timing
    trans_right_high_to = licks_r_high_to - stimulus_timing
    trans_left_high_to = licks_l_high_to - stimulus_timing
    trans_left_low_to = licks_l_low_to - stimulus_timing
    trans_right_low_to = licks_r_low_to - stimulus_timing

    '''Step 3: Plot data'''
    # Plot heatmap of successful trials
    # Plot heatmap of successful trials
    fig1, figure1 = plt.subplots(2)
    fig1.supylabel("Trial number")
    fig1.supxlabel("Time points of licks relative to stimulus delivery")
    fig1.suptitle("Heat map of licks in successful trials")
    figure1[0].vlines(0, color='r',
                   ymin=0, ymax=number_of_trials,
                   label='Stimulus delivery time')
    figure1[1].vlines(0, color='r',
                   ymin=0, ymax=number_of_trials,
                   label='Stimulus delivery time')
    figure1[0].plot(np.transpose(trans_high_success),
                    np.array([np.arange(trans_high_success.shape[0])]*trans_high_success.shape[1]),
                    'k.')
    figure1[0].set_ylabel('Trial number')
    figure1[0].set_xlabel('Seconds')
    #figure1[0].set_title('High stimulus amplitude trials')
    figure1[0].set_title('Timing licks in high amplitude session')
    figure1[1].plot(np.transpose(trans_low_success),
                    np.array([np.arange(trans_low_success.shape[0])]*trans_low_success.shape[1]),
                    'k.')
    figure1[1].set_title('Low stimulus amplitude trials')
    figure1[0].legend(loc='best')
    figure1[1].legend(loc='best')
    # Plot heatmap for high stimulus time out trials: correct (rightwards) licks in black,
    # incorrect (leftwards) licks in green
    fig2, figure2 = plt.subplots(1)
    plt.ylabel("Trial number")
    plt.xlabel("Timing of licks relative to stimulus delivery time, black for rightward licks, red for leftward licks")
    plt.title("Heat map of licks in high stimulus trials with time out")
    figure2.plot(np.transpose(trans_right_high_to),
                 (np.array([np.arange(trans_right_high_to.shape[0])] * trans_right_high_to.shape[1])),
                 'k.')
    figure2.plot(np.transpose(trans_left_high_to),
                 np.array([np.arange(trans_left_high_to.shape[0])] * trans_left_high_to.shape[1]),
                 'r.')
    figure2.vlines(0, color='y',
                   ymin=0, ymax=number_of_trials, label='Stimulus delivery time')
    figure2.legend(loc='best')
    # Plot heatmap for low stimulus time out trials: correct licks (leftwards) in black,
    # incorrect licks (rightwards) in red
    fig3, figure3 = plt.subplots(1)
    plt.ylabel("Trial number")
    plt.xlabel("Timing of licks relative to ITI2, black for leftward licks, red for rightward licks")
    plt.title("Heat map of licks in low stimulus trials with time outs")
    figure3.plot(np.transpose(trans_left_low_to),
                 np.array([np.arange(trans_left_low_to.shape[0])] * trans_left_low_to.shape[1]),
                 'k.')
    figure3.plot(np.transpose(trans_right_low_to),
                 np.array([np.arange(trans_right_low_to.shape[0])] * trans_right_low_to.shape[1]),
                 'r.')
    figure3.vlines(0, color='y',
                   ymin=0, ymax=number_of_trials,
                   label='Stimulus delivery time')
    figure3.legend(loc='best')
    fig1.savefig(str(my_dirname) + "/HeatmapHITTrials")
    fig1.show()
    fig2.savefig(str(my_dirname) + "/HeatmapHighStimulusTO")
    fig2.show()
    fig3.savefig(str(my_dirname) + "/HeatmapLowStimulusTO")
    fig3.show()

def priors_analysis_2afc(ma_path):
    """ (Adinda)
    This function returns info_Priors.json, which contains
    1) = [0]
    for the case of a previous right success trial, the probability of a
    - HIT trial
    - successful right lick trial
    - Time out for right lick trial (so wrong classification as high amplitude = Low TO)
    2) = [1]
    for the case of a previous left success trial, the probability of a:
    - HIT trial
    - successful left trial
    - Time out for left lick (so wrong classification as low amplitude = High TO)
    3) = [2]
    the number of trials following a right success trial that are
    - HIT
    - successful right
    - TO for right lick (wrong classification as high amplitude)
    4) = [3]
    the number of trials following a left success trial that are
    - HIT
    - successful left
    - TO for left lick (wrong classification as low amplitude)
    5) = [4]
    the total amount of trials following
    - a right success
    - left success"""
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