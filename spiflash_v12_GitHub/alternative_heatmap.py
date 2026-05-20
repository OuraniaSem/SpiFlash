import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from psycho import save_eventDico_json as save_eventPsycho_json
from main_function_Sp import catch_info_xls, catch_info_json, search_nb_newtrial, search_nb_endtrial, \
    diff_new_end_trial, liste_freq_amp

directory_ = ("C:/Users/Adinda/Documents/Thesis/Data/5143_5148_5149/5143_5148_5149/5143/20230316_5143_2AFC_Training_Day18/20230316-105510/20230316-105510.xls")



def alternative_heatmap_2afc(xl_path):
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
                    missed_trial = False
                if xls_data.iloc[position][4] == 'Timeout' and xls_data.iloc[position][0] == 'TRANSITION':
                    high_to_trials.append(counter_trials)
                    trial_type[counter_trials] = 'HighTO'
                    missed_trial = False
            # For low amplitude stimulus trials
            if my_data_json[counter_trials].get('trial_type') == "low":
                if xls_data.iloc[position][4] == 'Reward_left' and xls_data.iloc[position][0] == 'TRANSITION':
                    low_success_trials.append(counter_trials)
                    trial_type[counter_trials] = 'LowSuccess'
                    missed_trial = False
                if xls_data.iloc[position][4] == 'Timeout' and xls_data.iloc[position][0] == 'TRANSITION':
                    low_to_trials.append(counter_trials)
                    trial_type[counter_trials] = 'LowTO'
                    missed_trial = False
        if missed_trial is True:
            trial_type[counter_trials] = 'Miss'

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
    licks_miss = np.empty((number_of_trials, max_licks_trial))
    licks_miss[:] = np.NaN

    for trial in range(number_of_trials):  # For every trial
        # Set counter for each category of trial to 0
        count_high_success = 0
        count_r_high_to = 0
        count_l_high_to = 0
        count_low_success = 0
        count_r_low_to = 0
        count_l_low_to = 0
        count_low_miss = 0
        count_high_miss = 0
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
                elif trial_type[trial] == "Miss":
                    # Rightward lick
                    if xls_data.iloc[position][4] == 94:
                        licks_miss[trial, count_high_miss] = time_lick
                        count_high_miss += 1
                    # Lick was leftwards
                    else:
                        licks_miss[trial, count_low_miss] = time_lick
                        count_low_miss += 1

    ''' Step 2: Transform lick time data relative to Stimulus_timing data, 
    so that stimulus delivery time t= 0 for every trial'''
    trans_high_success = licks_high_success - stimulus_timing
    trans_low_success = licks_low_success - stimulus_timing
    trans_right_high_to = licks_r_high_to - stimulus_timing
    trans_left_high_to = licks_l_high_to - stimulus_timing
    trans_left_low_to = licks_l_low_to - stimulus_timing
    trans_right_low_to = licks_r_low_to - stimulus_timing
    trans_miss = licks_miss - stimulus_timing
    print('licks_miss', licks_miss[1])
    print('Stimulus timing', stimulus_timing[1])
    print(trans_miss[1])

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
                    np.array([np.arange(trans_high_success.shape[0])] * trans_high_success.shape[1]),
                    'k.')
    figure1[0].set_ylabel('Trial number')
    figure1[0].set_xlabel('Seconds')
    # figure1[0].set_title('High stimulus amplitude trials')
    figure1[0].set_title('Timing licks in high amplitude session')
    figure1[1].plot(np.transpose(trans_low_success),
                    np.array([np.arange(trans_low_success.shape[0])] * trans_low_success.shape[1]),
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
    # Plot heatmap of missed trials
    fig4, figure4 = plt.subplots(2)
    fig4.supylabel("Trial number")
    fig4.supxlabel("Time points of licks relative to stimulus delivery")
    fig4.suptitle("Heat map of licks in missed trials")
    figure4[0].vlines(0, color='r',
                   ymin=0, ymax=number_of_trials,
                   label='Stimulus delivery time')
    figure4[1].vlines(0, color='r',
                   ymin=0, ymax=number_of_trials,
                   label='Stimulus delivery time')
    figure4[0].plot(np.transpose(trans_miss),
                    np.array([np.arange(trans_miss.shape[0])]*trans_miss.shape[1]),
                    'k.')
    figure4[0].set_ylabel('Trial number')
    figure4[0].set_xlabel('Seconds')

    fig4.show()
    fig4.savefig(str(my_dirname) + "/HeatmapMissedTrials")
    print('Stimulus timing', stimulus_timing)
    print('licks miss', licks_miss)
