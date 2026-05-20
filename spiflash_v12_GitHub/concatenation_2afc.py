import json
import os
import numpy as np
import matplotlib.pyplot as plt
from psycho import sigmoid
from scipy.optimize import curve_fit, fsolve
from scipy.stats import linregress, norm
from collections import Counter

from scipy.optimize import brentq

#directory_ = (['C:/Users/Adinda/Documents/Thesis/PyBpod/Concat_testdata/wrap_2afc20230317-172937.json', 'C:/Users/Adinda/Documents/Thesis/PyBpod/Concat_testdata/wrap_2afc20230317-172938.json', 'C:/Users/Adinda/Documents/Thesis/PyBpod/Concat_testdata/wrap_2afc20230317-172939.json'], 'All Files (*)')

#Tryout_ = (['C:/Users/Adinda/Documents/Thesis/Data/Concatenation_Data/5380_ConcatenationDisc/wrap_2afc20230602-112342.json', 'C:/Users/Adinda/Documents/Thesis/Data/Concatenation_Data/5380_ConcatenationDisc/wrap_2afc20230602-114406.json'], 'All Files (*)')
def get_sensitivity_2afc(the_dico):
    right_success = (the_dico['Reward High'] / (the_dico['Reward High'] + the_dico['Miss High'] + the_dico['Timeout High']))
    if right_success == 1:
        right_success = 0.99
    if right_success == 0:
        right_success = 0.01

    right_fail = (the_dico['Timeout High'] / (the_dico['Reward High'] + the_dico['Miss High'] + the_dico['Timeout High']))
    if right_fail == 1:
        right_fail = 0.99
    if right_fail == 0:
        right_fail = 0.01

    left_success = (the_dico["Reward Low"] / (the_dico["Reward Low"] + the_dico["Miss Low"] + the_dico["Timeout Low"]))
    if left_success == 1:
        left_success = 0.99
    if left_success == 0:
        left_success = 0.01

    left_fail = (the_dico["Timeout Low"] / (the_dico["Reward Low"] + the_dico["Miss Low"] + the_dico["Timeout Low"]))
    if left_fail == 1:
        left_fail = 0.99
    if left_fail == 0:
        left_fail = 0.01

    Hit_rate = (the_dico['Reward High'] + the_dico['Reward Low']) / (the_dico['Reward High'] + the_dico['Miss High'] + the_dico['Timeout High'] + the_dico['Reward Low'] + the_dico['Miss Low'] + the_dico['Timeout Low'])
    if right_fail == 1:
        right_fail = 0.99
    if right_fail == 0:
        right_fail = 0.01

    FA_rate = (the_dico['Timeout High'] + the_dico['Timeout Low']) / (the_dico['Reward High'] + the_dico['Miss High'] + the_dico['Timeout High'] + the_dico['Reward Low'] + the_dico['Miss Low'] + the_dico['Timeout Low'])
    if right_fail == 1:
        right_fail = 0.99
    if right_fail == 0:
        right_fail = 0.01

    print('right success = ', right_success)
    print('left success = ', left_success)
    s_high = 0.70710678118*((norm.ppf(right_success)) - (norm.ppf(right_fail)))
    s_high = float("{:.3f}".format(s_high))
    s_low = 0.70710678118*((norm.ppf(left_success)) - (norm.ppf(left_fail)))
    s_low = float("{:.3f}".format(s_low))
    s = 0.70710678118*(norm.ppf(Hit_rate)) - (norm.ppf(FA_rate))
    s = float("{:.3f}".format(s))
    c = s_high - s_low
    c = float("{:.3f}".format(c))
    # s = (norm.ppf(right_success)) - (norm.ppf(left_success)) old way to calculate
    # s = float("{:.3f}".format(s)) old way to calculate
    # c = - (norm.ppf(right_success)) + (norm.ppf(left_success)) / 2
    # c = float("{:.3f}".format(c))
    print('norm right success', norm.ppf(right_success))
    print(' norm left success', norm.ppf(left_success))
    dico_sensitivity = {"sensitivity": s, "Sensitivity_high": s_high, "Sensitivity_low": s_low, "criterion": c}
    sensitivity = "Sensitivity : " + str(s)
    return sensitivity, dico_sensitivity


def save_concat_barplot_json(the_dico, directory_name):
    with open(str(directory_name) + '/Concatenation_infoBarplot.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)


def save_concat_psycho_json(the_dico, directory_name):
    with open(str(directory_name) + '/Concatenation_infoPsycho.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)


def save_concat_priors_json(the_dico, directory_name):
    with open(str(directory_name) + '/Concatenation_infoPriors.json', 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)


def find_x_for_y_0_5(x, x0, k):
    return(sigmoid(x, x0, k)) - 0.5


def barplot_2afc_concat(directory):
    """Generates the barplot for concatenated data. Takes as input the directory of the wrap.json files"""
    # Extract the barplot information for each session from each wrap json file
    # And append into one big list: info_barplot_session
    info_barplot_session = []
    for icount_json in range(len(directory[0])):
        with open(directory[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_barplot_session.append(info_json[0][0])

    # Get the total occurrence of events over all sessions
    total_barplot_events = {"Reward Low": 0, "Reward High": 0, "Miss Low": 0, "Miss High": 0, "Timeout Low": 0,
                            "Timeout High": 0}
    for count_event in range(len(info_barplot_session)):
        total_barplot_events["Reward Low"] += info_barplot_session[count_event]["Reward Low"]
        total_barplot_events["Reward High"] += info_barplot_session[count_event]["Reward High"]
        total_barplot_events["Miss Low"] += info_barplot_session[count_event]["Miss Low"]
        total_barplot_events["Miss High"] += info_barplot_session[count_event]["Miss High"]
        total_barplot_events["Timeout Low"] += info_barplot_session[count_event]["Timeout Low"]
        total_barplot_events["Timeout High"] += info_barplot_session[count_event]["Timeout High"]
    print("total barplot events are", total_barplot_events)

    # Get the percentages
    total_trials = sum(total_barplot_events.values())
    x_names = []
    percent_x_values = []
    for key, values in total_barplot_events.items():
        x_names.append(key)
        final_results = (values * 100) / total_trials
        final_results = float("{:.2f}".format(final_results))
        percent_x_values.append(final_results)
    print('percentages', percent_x_values)

    sensitivity = get_sensitivity_2afc(total_barplot_events)

    # Plot the barplot
    plt.rcParams.update({'font.size': 10})
    plt.rcParams["figure.figsize"] = (10, 4)

    ax = plt.subplot(111)
    ax.set_ylim(0, 100)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.bar(x_names, percent_x_values)
    ax.title.set_text("Concatenation Barplot")

    plt.tight_layout()
    plt.show()

    # Save the info of the concatenated barplot
    # First find the correct directory
    for icount_name_files in range(len(directory[0])):
        dirname, basename = os.path.split(directory[0][icount_name_files])
    # Then save the info
    save_concat_barplot_json([total_barplot_events, sensitivity], dirname)


def psycho_2afc_concat(directory):

    """Takes as input the directory of the wrap.json files
    Generates the psychometric for concatenated data
    And saves the json file Concatenated_infoPsycho, which returns for each amplitude:
    - [0]: total # right trials
    - [1]: total # left trials
    - [2]: total # miss trials
    - [3]: total # trials
    - [4]: list of the amplitudes for which data exists
    - [5]: frequency right trials
    - [6]: frequency left trials
    - [7]: frequency of miss trials
    - [8]: slope of the fitted sigmoid
    """
    # Extract the psycho information for each session from each wrap json file
    # And append into one big list: info_psycho_session
    info_psycho_session = []

    for icount_json in range(len(directory[0])):
        with open(directory[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_psycho_session.append(info_json[2])
    # Get the amplitudes used (just look at the first session)
    amplitude_list = info_psycho_session[0][4]

    # Make lists for the #right, # left, # miss and amplitudes
    trials_right = {}
    trials_left = {}
    trials_missed = {}
    tot_trials_amplitudes = {}

    for icount_amp_liste in range(len(amplitude_list)):
        trials_right[amplitude_list[icount_amp_liste]] = 0
        trials_left[amplitude_list[icount_amp_liste]] = 0
        trials_missed[amplitude_list[icount_amp_liste]] = 0
        tot_trials_amplitudes[amplitude_list[icount_amp_liste]] = 0
    print('trials right before adding', trials_right)
    # Extract and sum the trial types of all sessions & add to the dicts
    for i in range(len(info_psycho_session)):
        trials_right = dict((Counter(trials_right) + Counter(info_psycho_session[i][0])))
        trials_left = dict((Counter(trials_left) + Counter(info_psycho_session[i][1])))
        trials_missed = dict((Counter(trials_missed) + Counter(info_psycho_session[i][2])))
        tot_trials_amplitudes = dict((Counter(tot_trials_amplitudes) + Counter(info_psycho_session[i][3])))
    print('trials right after adding', trials_right)
    # Get frequencies
    '''Calculate frequency types of trials from trials with this stimulus amplitude'''
    freq_right = {k: trials_right[k] / float(tot_trials_amplitudes[k]) for k in tot_trials_amplitudes if k in
                  trials_right}
    freq_left = {k: trials_left[k] / float(tot_trials_amplitudes[k]) for k in tot_trials_amplitudes if k in trials_left}
    freq_miss = {k: trials_missed[k] / float(tot_trials_amplitudes[k]) for k in tot_trials_amplitudes if k in
                 trials_missed}
    print('freq_right', freq_right)
    # Generate plot
    xdata = list(freq_right.keys())
    xdata = [float(x) for x in xdata]
    #print('xdata =', xdata)
    ydata = list(freq_right.values())
    #print('ydata =', ydata)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(xdata, ydata, 'k.', label='data')
    ax.set_ylim(0, 1)
    ax.set_xlabel('Amplitude of stimulus')
    ax.set_ylabel('Frequency of rightward lick response trials')
    ax.set_title('Psychometric curve')

    # Get sigmoid fit
    if len(amplitude_list) >= 3:
        popt, pcov = curve_fit(sigmoid, xdata, ydata, maxfev=3000)
        fix_value = amplitude_list[-1] + 0.1
        x = np.linspace(0, fix_value, 500)
        y = sigmoid(x, *popt)
        ax.plot(x, y, label='fit')

        # Find the y-value for which X = 0.5 to determine the discriminatio threshold
        x_for_y_0_5 = fsolve(find_x_for_y_0_5, x0=0, args=(popt[0], popt[1]))
        print("")
        print("The value for y=0.5 is : ", x_for_y_0_5[0])
        print("")
        ax.vlines(x_for_y_0_5, 0, 10)
        x_for_y_0_5 = x_for_y_0_5.tolist()[0]
        #print(x_for_y_0_5)

        x0, k = popt
        inflection_point = x0
        print("")
        print("The inflection point is : ", inflection_point)
        print("")

        # Set max x range slightly above highest tested amplitude (at 3 if highest amplitude was 2.88)
        xmax = amplitude_list[-1] + 0.12
        ax.set_xlim(1, xmax)

        # Extract slope
        slope_polyfit, intercept_polyfit = np.polynomial.Polynomial.fit(x, y, deg=1)
        print("slope polyfit: " + str(slope_polyfit))
        slope_linregress, intercept, r_value, p_value, std_err = linregress(x, y)
        #print("slope linregress: " + str(slope_linregress))
        slope, intercept = np.polyfit(x, y, 1)
        dico_psycho = {"Slope": slope, "Discrimination threshold": x_for_y_0_5, "inflection point": float("{:.2f}".format(inflection_point))}
        print("slope np: " + str(slope))

    plt.show()

    # Find the correct directory to save the json file and figure in
    for icount_name_files in range(len(directory[0])):
        dirname, basename = os.path.split(directory[0][icount_name_files])
    # and save info in Concatenated_info_psycho and ConcatenatedPsychometricCurve
    concatenated_info_psycho = [dico_psycho, trials_right, trials_left, trials_missed, tot_trials_amplitudes, amplitude_list,
                                freq_right, freq_left, freq_miss]
    save_concat_psycho_json(concatenated_info_psycho, dirname)
    plt.savefig(str(dirname) + "/ConcatenatedPsychometricCurve")


def priors_2afc_concat(directory):
    # Extract the priors information for each session from each wrap json file
    # And append into one big list: info_priors_sessions
    info_priors_sessions = []
    for icount_json in range(len(directory[0])):
        with open(directory[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_priors_sessions.append(info_json[3])

    # Extract and sum the number of trial types following right trials over all sessions
    prior_right_success_dico = {"Hit after right": 0, "Hit right after right": 0, "Timeout left after right": 0}
    prior_left_success_dico = {"Hit after left": 0, "Hit left after left": 0, "Timeout right after left": 0}
    number_after_success = {"Trials after right success": 0, "Trials after left success": 0}

    for i in range(len(info_priors_sessions)):
        prior_right_success_dico = dict((Counter(prior_right_success_dico) + Counter(info_priors_sessions[i][2])))
        prior_left_success_dico = dict((Counter(prior_left_success_dico) + Counter(info_priors_sessions[i][3])))
        number_after_success = dict((Counter(number_after_success) + Counter(info_priors_sessions[i][4])))

    # Calculate the frequencies of trial types occurring after a right or left success trial
    freq_after_rightsuccesslist = []
    freq_after_leftsuccesslist = []
    after_rightsuccess_names = ["Freq hit after right success", "Freq hit right after right successs",
                                "Freq timeout left after right success"]
    after_leftsuccess_names = ["Freq hit after left success", "Freq hit left after left success",
                               "Freq timeout right after left success"]
    # For trials following right success trials
    for key, values in prior_right_success_dico.items():
        frequencies_right = values / number_after_success["Trials after right success"]
        frequencies_right = float("{:.2f}".format(frequencies_right))
        freq_after_rightsuccesslist.append(frequencies_right)
    freq_after_right_success = {i: j for i, j in zip(after_rightsuccess_names, freq_after_rightsuccesslist)}
    # For trials following left success trials
    for key, values in prior_left_success_dico.items():
        frequencies_left = values / number_after_success["Trials after left success"]
        frequencies_left = float("{:.2f}".format(frequencies_left))
        freq_after_leftsuccesslist.append(frequencies_left)
    freq_after_left_success = {i: j for i, j in zip(after_leftsuccess_names, freq_after_leftsuccesslist)}
    print('freq_after_right_success', freq_after_right_success)
    print('freq_after_left_success', freq_after_left_success)

    # Find the correct directory to save the json file in & save info
    for icount_name_files in range(len(directory[0])):
        dirname, basename = os.path.split(directory[0][icount_name_files])
    dico = [freq_after_right_success, freq_after_left_success, prior_left_success_dico, number_after_success]
    save_concat_priors_json(dico, dirname)

#priors_2afc_concat(directory_)
#psycho_2afc_concat(directory_)
#barplot_2afc_concat(directory_)

#psycho_2afc_concat(Tryout_)