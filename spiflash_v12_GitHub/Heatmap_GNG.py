'''(Adinda)
Function to obtain a heat map of the timepoints at which the mouse licks over different trials for the Go-NoGo task
Y-axis: trials, X-axis: time relative to stimulus delivery per trial
Note: in line 111, the ITI2 is hardcoded at 2 --> when the experiment uses a different
 timing of the ITI2, make sure to change this!'''
import json
import math
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import main_function_Sp
from main_function_Sp import search_nb_newtrial, search_nb_endtrial, diff_new_end_trial, catch_info_xls, catch_info_json

def Heatmap_GNG(xl_path):
    # get the info from the Excel file
    Xls_data, my_dirname = catch_info_xls(xl_path)
    # get the info from json file
    my_data_json = catch_info_json(my_dirname)
    number_of_trials = len(my_data_json)
    '''Step 1 consists of extracting all the necessary info from our Excel and json file.
    We wish to identify the timing of each lick per trial, as well as the timing the stimulus was given in each trial
    These variables will be stored in LicksPerTrial and Stimulus_timing respectively'''
    number_of_trials = len(my_data_json)
    # Get the line number for the beginning and ending of each trial
    Start_trials = search_nb_newtrial(Xls_data, number_of_trials)
    End_trials = search_nb_endtrial(Xls_data, number_of_trials)
    # Get number of lines between the start & end of each trial
    Start_to_end_trials = diff_new_end_trial(Start_trials, End_trials)

    # Get the max number of licks in a trial: Identify the licks in time for each trial
    NumberLicksPerTrial = []  # Make an empty array to store the number of licks for each trial
    for CounterTrials in range(number_of_trials):  # For every trial
        CounterLicks = 0  # Set counter to 0
        for WithinTrials in range(
                Start_to_end_trials[CounterTrials]):  # Looping over every line corresponding to said trial
            # Find the position of the line we want to look for info in the excell file
            Position = Start_trials[CounterTrials] + WithinTrials
            # 94 means the red laser infrabeam was interrupted, corresponding to a lick event of the mouse
            if Xls_data.iloc[Position][4] == 94:
                CounterLicks += 1
        NumberLicksPerTrial.append(CounterLicks)
    MaxLicksPerTrial = max(NumberLicksPerTrial)

    # Make empty array to put the stimulus time in for each trial (again each row will represent a trial)
    Stimulus_timing = np.zeros((number_of_trials, 1))  # zeroes because some trials never get stimulus after time-outs!

    TrialType = np.empty(number_of_trials)
    TrialType = TrialType.tolist()
    StimulusGoTrials = []
    TOGoTrials = []
    NoGoTrials = []
    '''Step 1.a: identify between
    - NoGo trials (regardless of timeout or not)
    - Go Trials where a stimulus was given
    - Go Trials with time outs'''
    for CounterTrials in range(number_of_trials):  # For every trial
        if my_data_json[CounterTrials].get('trial_type') == "Go":  # Identify whether trial should have been Go trial
            for WithinTrials in range(Start_to_end_trials[CounterTrials]):  # For every line corresponding to said trial
                # Identify the position of the line we want to look for info in the excell file
                Position = Start_trials[CounterTrials] + WithinTrials
                # Identify whether stimulus was given, and if so add trial number to list StimulusGoTrials
                if Xls_data.iloc[Position][4] == 'Stimulus' and Xls_data.iloc[Position][0] == 'TRANSITION':
                    Timing = Xls_data.iloc[Position][2]
                    Stimulus_timing[CounterTrials, 0] = Timing
                    StimulusGoTrials.append(CounterTrials)
                    TrialType[CounterTrials] = "StimulusGoTrial"
                # Identify whether there was a timeout instead, if so add trial number to list TOGoTrials
                if Xls_data.iloc[Position][4] == 'Timeout' and Xls_data.iloc[Position][0] == 'TRANSITION':
                    TOGoTrials.append(CounterTrials)
                    TrialType[CounterTrials] = "TOGoTrial"
        if my_data_json[CounterTrials].get('trial_type') == "Nogo":  # Identify trial as NoGo trial
            NoGoTrials.append(CounterTrials)
            TrialType[CounterTrials] = "NoGoTrial"

    '''Step 1.b Identify the lick times for each trial and add to corresponding matrix'''
    # Make empty matrices to put lick times in for each trial, depending on the trial type
    LicksStimulusGoTrials = np.empty((number_of_trials, MaxLicksPerTrial))
    LicksStimulusGoTrials[:] = np.NaN
    LicksTOGoTrials = np.empty((number_of_trials, MaxLicksPerTrial))
    LicksTOGoTrials[:] = np.NaN
    LicksNoGoTrials = np.empty((number_of_trials, MaxLicksPerTrial))
    LicksNoGoTrials[:] = np.NaN

    for Trial in range(number_of_trials):  # For every trial
        # Set counter for each category of trial to 0
        CountStimGo = 0
        CountTOGo = 0
        CountNoGo = 0
        for WithinTrials in range(Start_to_end_trials[Trial]):  # And every line corresponding to said trial
            # Identify the position of the line we want to look for info in the excell file
            Position = Start_trials[Trial] + WithinTrials
            # Check if there was a lick in this line
            if Xls_data.iloc[Position][4] == 94:
                # Find the corresponding time in column C of the excel file
                TimeLick = Xls_data.iloc[Position][2]
                # Check in which matrix the time value should be added
                if TrialType[Trial] == "StimulusGoTrial":  # For Go trials with stimulus delivered
                    LicksStimulusGoTrials[Trial, CountStimGo] = TimeLick
                    CountStimGo += 1
                elif TrialType[Trial] == "TOGoTrial":  # For Go trials with a timeout & thus no stimulus delivered
                    LicksTOGoTrials[Trial, CountTOGo] = TimeLick
                    CountTOGo += 1
                elif TrialType[Trial] == "NoGoTrial":
                    LicksNoGoTrials[Trial, CountNoGo] = TimeLick
                    CountNoGo += 1

    '''Step 2: Transform lick time data depending on category of trial'''
    # For Go trial with stimulus delivery: transform time points so that Stimulus delivery time t = 0
    TransLicksStimGo = LicksStimulusGoTrials - Stimulus_timing
    # For Go trial with time out: transform data so that ITI2 time t = 0
    ITI2 = 2  # Hardcoded because in pybod ITI2 will always be delivered at t=2 (update this in case you change the program)
    TransLickTOGo = LicksTOGoTrials - ITI2
    # For NoGo trials:
    TransLickNoGo = LicksNoGoTrials - ITI2

    '''Step 3: Plot data'''
    # Plot heatmap of Go trials with stimulus delivery
    fig1, figure1 = plt.subplots(1)
    plt.ylabel("Trial number")
    plt.xlabel("Timing of licks relative to stimulus delivery time in seconds")
    plt.title("Heat map of licks for Go trials with stimulus delivery")
    figure1.plot(np.transpose(TransLicksStimGo),
                 np.array([np.arange(TransLicksStimGo.shape[0])] * TransLicksStimGo.shape[1]),
                 'k.')
    figure1.vlines(0, color='r',
                   ymin=0, ymax=number_of_trials,
                   label='Stimulus delivery time')
    figure1.legend(loc='best')
    # Plot heatmap of Go trials with time out
    fig2, figure2 = plt.subplots(1)
    plt.ylabel("Trial number")
    plt.xlabel("Timing of licks relative to ITI2")
    plt.title("Heat map of licks for Go trials with a time out")
    figure2.plot(np.transpose(TransLickTOGo),
                 np.array([np.arange(TransLickTOGo.shape[0])] * TransLickTOGo.shape[1]),
                 'k.')
    figure2.vlines(0, color='b',
                   ymin=0, ymax=number_of_trials,
                   label='Start of ITI2')
    figure2.legend(loc='best')
    # Plot heatmap of NoGo trials
    fig3, figure3 = plt.subplots(1)
    plt.ylabel("Trial number")
    plt.xlabel("Timing of licks relative to ITI2")
    plt.title("Heat map of licks for No Go trials")
    figure3.plot(np.transpose(TransLickNoGo),
                 np.array([np.arange(TransLickNoGo.shape[0])] * TransLickNoGo.shape[1]),
                 'k.')
    figure3.vlines(0, color='b',
                   ymin=0, ymax=number_of_trials,
                   label='Start of ITI2')
    figure3.legend(loc='best')
    fig1.savefig(str(my_dirname) + "/HeatmapGOStim.svg")
    fig2.savefig(str(my_dirname) + "/HeatmapGOTimeOut")
    fig3.savefig(str(my_dirname) + "/HeatmapNOGO")