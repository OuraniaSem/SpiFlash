import json
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.utils import info
from barplot import get_sensitivity
import itertools
from weibull_S import plot_things_weibull
import collections, functools, operator
from psycho import sigmoid
from scipy.optimize import curve_fit, fsolve
from statistics import mean, pstdev
from scipy.stats import linregress

def find_x_for_y_0_5(x, x0, k):
    return sigmoid(x, x0, k) - 0.5

def calcul_pourcent_liste(petit_dico):
        pourcent_liste = []
        for key, values in petit_dico.items():
                total = sum(petit_dico.values())
                print(total)
                final_results = (values * 100)/ total
                final_results = float("{:.2f}".format(final_results))
                pourcent_liste.append(final_results)
        
        return pourcent_liste

def barplot_concatenation(myFile_json):
    event_barplot = {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, "NOgo_false alarm" : 0, "NOgo_rejection" : 0, "NOgo_timeout_paw" : 0}
    total_barplot = 0
    x_names = []
    pourcent_x_values = []
    pourcent_x_values_total = []
    liste_legende = []

    info_barplot = []
    for icount_json in range(len(myFile_json[0])):
        with open(myFile_json[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_barplot.append(info_json[0][0])
            print(info_barplot)
    
    for icount_name_files in range(len(myFile_json[0])):
        dirname, basename = os.path.split(myFile_json[0][icount_name_files])
        liste_legende.append(basename)
    
    liste_legende.append("Concatenation")
    print(liste_legende)

    for incout_event in range(len(info_barplot)):
        event_barplot["GO_hit"] += info_barplot[incout_event]["GO_hit"]
        event_barplot["GO_miss"] += info_barplot[incout_event]["GO_miss"]
        event_barplot["GO_timeout"] += info_barplot[incout_event]["GO_timeout"]
        event_barplot["NOgo_false alarm"] += info_barplot[incout_event]["NOgo_false alarm"]
        event_barplot["NOgo_rejection"] += info_barplot[incout_event]["NOgo_rejection"]
        event_barplot["NOgo_timeout_paw"] += info_barplot[incout_event]["NOgo_timeout_paw"]

    for key, values in event_barplot.items():
        total_barplot += values
        x_names.append(key)

    pourcent_event_total = calcul_pourcent_liste(event_barplot)

    for icount_dico in range(len(info_barplot)):
        pourcent_x_values = calcul_pourcent_liste(info_barplot[icount_dico])
        pourcent_x_values_total.append(pourcent_x_values)
    
    pourcent_x_values_total.append(pourcent_event_total)

    my_sensitivity, sensitivity_dico = get_sensitivity(event_barplot)
    print(my_sensitivity)
    print(pourcent_x_values)
    print("Concatenation : ", pourcent_event_total)

    dico_info_final = []
    for icount_barplot_concatenation in range (len(info_barplot)):
        dico_concatenation_barplot = [{"name" : liste_legende[icount_barplot_concatenation]}, 
        info_barplot[icount_barplot_concatenation]]
        dico_info_final.append(dico_concatenation_barplot)


    with open(str(dirname) + '/infoBarplotConcatenation.json', 'w') as jsonFile:
        json.dump(dico_info_final, jsonFile, indent=4)

    # set width of bars
    barWidth = 0.1

    # Set position of bar on X axis
    r = np.arange(len(pourcent_x_values_total[0]))

    plt.rcParams.update({'font.size': 10})
    plt.rcParams["figure.figsize"] = (13,4)

    ax = plt.subplot(111)
    ax.set_ylim(0,100)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for icount_ax in range(len(pourcent_x_values_total)):
        ax.bar(r, pourcent_x_values_total[icount_ax], width=0.05, align='center', label= liste_legende[icount_ax])
        r = [x + barWidth for x in r]

    # Add xticks on the middle of the group bars
    plt.xticks([r + barWidth for r in range(len(pourcent_x_values_total[0]))], x_names)
    
    #plt.legend()
    plt.tight_layout()
    plt.show()

def barplot_concatenation_only(myFile_json):
    event_barplot = {"GO_hit" : 0, "GO_miss" : 0, "GO_timeout" : 0, "NOgo_false alarm" : 0, "NOgo_rejection" : 0, "NOgo_timeout_paw" : 0}
    total_barplot = 0
    x_names = []
    pourcent_x_values = []
    info_barplot = []
    liste_legende = []

    for icount_json in range(len(myFile_json[0])):
        with open(myFile_json[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_barplot.append(info_json[0][0])
            print(info_barplot)
    
    for icount_name_files in range(len(myFile_json[0])):
        dirname, basename = os.path.split(myFile_json[0][icount_name_files])
        liste_legende.append(basename)
    

    for incout_event in range(len(info_barplot)):
        event_barplot["GO_hit"] += info_barplot[incout_event]["GO_hit"]
        event_barplot["GO_miss"] += info_barplot[incout_event]["GO_miss"]
        event_barplot["GO_timeout"] += info_barplot[incout_event]["GO_timeout"]
        event_barplot["NOgo_false alarm"] += info_barplot[incout_event]["NOgo_false alarm"]
        event_barplot["NOgo_rejection"] += info_barplot[incout_event]["NOgo_rejection"]
        event_barplot["NOgo_timeout_paw"] += info_barplot[incout_event]["NOgo_timeout_paw"]

    for key, values in event_barplot.items():
        total_barplot += values
        x_names.append(key)
    
    pourcent_event_total = calcul_pourcent_liste(event_barplot)

    for icount_dico in range(len(info_barplot)):
        pourcent_x_values = calcul_pourcent_liste(info_barplot[icount_dico])

    my_sensitivity, sensitivity_dico = get_sensitivity(event_barplot)
    print(my_sensitivity)
    print("Concatenation : ", pourcent_event_total)

    dico_info_barplot_concatenation_only = [event_barplot, sensitivity_dico]

    with open(str(dirname) + '/infoBarplotConcatenationOnly.json', 'w') as jsonFile:
        json.dump(dico_info_barplot_concatenation_only, jsonFile, indent=4)

    # set width of bars
    barWidth = 0.1

    plt.rcParams.update({'font.size': 10})
    plt.rcParams["figure.figsize"] = (10,4)

    ax = plt.subplot(111)
    ax.set_ylim(0,100)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.bar(x_names, pourcent_event_total)
    ax.title.set_text("Concatenation Barplot")

    # Add xticks on the middle of the group bars
    
    plt.tight_layout()
    plt.show()

def training_concatenation(myFile_json):
    info_training = []
    liste_legende = []

    for icount_json in range(len(myFile_json[0])):
        with open(myFile_json[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_training.append(info_json[1])
    
    #print(info_training)

    for icount_name_files in range(len(myFile_json[0])):
        dirname, basename = os.path.split(myFile_json[0][icount_name_files])
        liste_legende.append(basename)

    liste_x_names_total = []
    for icount_taille_liste in range (len(info_training)):
        liste_x_names = []
        for icount_x in range(0, len(info_training[icount_taille_liste]) * 10, 10):
                icount_x += 10
                liste_x_names.append(icount_x)
        liste_x_names_total.append(liste_x_names)

    pourcent_x_values_hit_total = []
    total_value_hit = []
    pourcent_x_values_timeout_total = []
    total_value_timeout = []

    total_trainig = 0

    for icount_total_training in range (len(info_training)):
        total_trainig += len(info_training[icount_total_training])

    for icount_len_liste in range (len(info_training)):
        pourcent_x_values_hit = []
        liste_x_values = []
        for icount_liste in range(len(info_training[icount_len_liste])):
            x_values = info_training[icount_len_liste][icount_liste]["GO_hit"]
            liste_x_values.append(x_values)
            final_results = (x_values*100) / 10
            final_results = float("{:.2f}".format(final_results))
            pourcent_x_values_hit.append(final_results)
        total_value_hit.append(liste_x_values)
        pourcent_x_values_hit_total.append(pourcent_x_values_hit)
    
    for icount_len_liste in range (len(info_training)):
        pourcent_x_values_timeout = []
        liste_x_values = []
        for icount_liste in range(len(info_training[icount_len_liste])):
            x_values = info_training[icount_len_liste][icount_liste]["GO_timeout"]
            liste_x_values.append(x_values)
            final_results = (x_values*100) / 10
            final_results = float("{:.2f}".format(final_results))
            pourcent_x_values_timeout.append(final_results)
        total_value_timeout.append(liste_x_values)
        pourcent_x_values_timeout_total.append(pourcent_x_values_timeout)
    
    #sum all the list with the number of HIT/TIMEOUT event
    sum_hit_values = [sum(x) for x in itertools.zip_longest(*total_value_hit, fillvalue=0)]
    sum_timeout_values = [sum(x) for x in itertools.zip_longest(*total_value_timeout, fillvalue=0)]

    liste_sum_x_values = []
    liste_sum_x_values_timeout = []
    pourcent_x_values_sum =[]
    pourcent_x_values_sum_timeout = []

    for icount_liste in range(len(sum_hit_values)):
        sum_x_values = sum_hit_values[icount_liste]
        sum_x_values_timeout = sum_timeout_values[icount_liste]
        liste_sum_x_values.append(sum_x_values)
        liste_sum_x_values_timeout.append(sum_x_values_timeout)
        final_results_sum = (sum_x_values*100) / total_trainig
        final_results_sum_timeout = (sum_x_values_timeout * 100) / total_trainig
        final_results_sum = float("{:.2f}".format(final_results_sum))
        final_results_sum_timeout = float("{:.2f}".format(final_results_sum_timeout))
        pourcent_x_values_sum.append(final_results_sum)
        pourcent_x_values_sum_timeout.append(final_results_sum_timeout)
    
    print("")
    print("print x values sum")
    print(pourcent_x_values_sum)
    print(len(pourcent_x_values_sum))
    print("")
    print("print x values sum timeout")
    print(pourcent_x_values_sum_timeout)
    print(len(pourcent_x_values_sum_timeout))
    print("")
    print("print x values timeout totale")
    print(pourcent_x_values_timeout_total)
    print(len(pourcent_x_values_timeout_total))

    print("")
    print(liste_x_names_total)
    print(liste_x_names_total[0])

    size_len_liste_names_total = 0
    index_len_listes_names_total = 0

    for icount_i in range(len(liste_x_names_total)):
        print(size_len_liste_names_total)
        print(len(liste_x_names_total[icount_i]))
        if size_len_liste_names_total < len(liste_x_names_total[icount_i]):
            index_len_listes_names_total = icount_i
            size_len_liste_names_total = len(liste_x_names_total[icount_i])
            icount_i += 1
        else:
            icount_i += 1


    linear_model_hit=np.polyfit(liste_x_names_total[index_len_listes_names_total],pourcent_x_values_sum,2)
    linear_model_fn_hit=np.poly1d(linear_model_hit)
    linear_model_timeout=np.polyfit(liste_x_names_total[index_len_listes_names_total], pourcent_x_values_sum_timeout,2)
    linear_model_fn_timeout=np.poly1d(linear_model_timeout)
    x_s=np.arange(0,liste_x_names_total[index_len_listes_names_total][-1])

    fig, axs = plt.subplots(2)
    for icount_liste_hit in range(len(pourcent_x_values_hit_total)):
        axs[0].plot(liste_x_names_total[icount_liste_hit], pourcent_x_values_hit_total[icount_liste_hit],"o", label= liste_legende[icount_liste_hit])
    
    axs[0].plot(x_s,linear_model_fn_hit(x_s),color="red", label = "Fit Hit")

    for icount_liste_timeout in range(len(pourcent_x_values_timeout_total)):
        axs[1].plot(liste_x_names_total[icount_liste_timeout], pourcent_x_values_timeout_total[icount_liste_timeout],"o", label= liste_legende[icount_liste_timeout])
    
    axs[1].plot(x_s,linear_model_fn_timeout(x_s),color="red", label = "Fit Hit")
    
    axs[0].title.set_text("Hit Concatenation")
    axs[0].set_xlabel('Number of trials')
    axs[0].set_ylabel('Hit (%)')
    axs[1].title.set_text("Timeout Concatenation")
    axs[1].set_xlabel('Number of trials')
    axs[1].set_ylabel('Timeout (%)')
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    axs[0].set_ylim([0, 100])
    axs[1].set_ylim([0, 100])

    #plt.legend()
    plt.tight_layout()
    plt.show()

def psycho_concatenation(myFile_json):
    info_psycho =[]
    liste_test_hit = []
    liste_test_total = []
    liste_final = []
    info_x_axis = []
    info_concatenation = []
    liste_hit_all = []
    liste_amp_all = []
    liste_legende = []
    

    for icount_json in range(len(myFile_json[0])):
        with open(myFile_json[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_psycho.append(info_json[2])
    
    for icount_name_files in range(len(myFile_json[0])):
        dirname, basename = os.path.split(myFile_json[0][icount_name_files])
        liste_legende.append(basename)
    
    print(info_psycho)
    for icount_data in range (len(info_psycho)):
        liste_hit_all.append(info_psycho[icount_data][2])
        liste_amp_all.append(info_psycho[icount_data][3])

    print(liste_hit_all)
    print(liste_amp_all)

    for icount in range (len(info_psycho)):
        liste_test_hit.append(info_psycho[icount][0])
        liste_test_total.append(info_psycho[icount][1])

    #result_hit = dict(functools.reduce(operator.add,
    #     map(collections.Counter, liste_test_hit)))
    result_hit = dict(functools.reduce(lambda a, b: a.update(b) or a,
                     liste_test_hit, collections.Counter()))

    #result_total = dict(functools.reduce(operator.add,
    #     map(collections.Counter, liste_test_total)))
    result_total = dict(functools.reduce(lambda a, b: a.update(b) or a,
                     liste_test_total, collections.Counter()))
  
    print("hit sum dico : ", str(result_hit))
    print("total sum dico : ", str(result_total))

    for (key1, value1), (key2, value2) in zip (result_hit.items(), result_total.items()):
        info_x_axis.append(float(key1))
        hit_rate_concatenation = value1 / value2
        hit_rate_concatenation = float("{:.2f}".format(hit_rate_concatenation))
        info_concatenation.append(hit_rate_concatenation)


    xdata = np.array(info_x_axis)
    ydata = np.array(info_concatenation)
    print(xdata)
    print(ydata)

    dico_info_final = []
    for icount_psycho_concatenation in range (len(info_psycho)):
        dico_concatenation_barplot = [{"name" : liste_legende[icount_psycho_concatenation]}, 
        info_psycho[icount_psycho_concatenation]]
        dico_info_final.append(dico_concatenation_barplot)

    with open(str(dirname) + '/infoPsychoConcatenation.json', 'w') as jsonFile:
        json.dump(dico_info_final, jsonFile, indent=4)

    popt, pcov = curve_fit(sigmoid, xdata, ydata, maxfev= 3000) # Scipy defines a value called maxfev, whose purpose is after how many iterations it gives up on the search (we can alter this parameter)
    fix_value = info_x_axis[-1] + 0.1

    x = np.linspace(0, fix_value, 50)
    y = sigmoid(x, *popt)

    slope, intercept = np.polyfit(x,y,1)
    print("slope np: "+ str(slope))

    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    print("slope linregress :" + str(slope))


    fig, axs = plt.subplots(1)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)

    axs.set_xlim(0,fix_value)
    axs.set_ylim(0,1)
    axs.plot(xdata, ydata, 'o', label='Concatenation')
    axs.plot(x,y,label='fit_WT')

    for icount_ax in range(len(liste_hit_all)):
        axs.plot(liste_hit_all[icount_ax], liste_amp_all[icount_ax], "o", label= liste_legende[icount_ax])

    #axs.legend(loc='best')
    axs.set_ylabel('Hit rate')


    plt.tight_layout()
    plt.show()

def psycho_concatenation_only(myFile_json):
    info_psycho =[]
    liste_test_hit = []
    liste_test_total = []
    liste_final = []
    info_x_axis = []
    info_concatenation = []
    liste_hit_all = []
    liste_amp_all = []
    liste_legende = []

    for icount_json in range(len(myFile_json[0])):
        with open(myFile_json[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_psycho.append(info_json[2])
    
    for icount_name_files in range(len(myFile_json[0])):
        dirname, basename = os.path.split(myFile_json[0][icount_name_files])
        liste_legende.append(basename)
    
    print(info_psycho)
    for icount_data in range (len(info_psycho)):
        liste_hit_all.append(info_psycho[icount_data][2])
        liste_amp_all.append(info_psycho[icount_data][3])

    print("liste hit")
    print(liste_hit_all)
    print("")
    print("liste amp")
    print(liste_amp_all)

    for icount in range (len(info_psycho)):
        liste_test_hit.append(info_psycho[icount][0])
        liste_test_total.append(info_psycho[icount][1])

    result_hit = dict(functools.reduce(lambda a, b: a.update(b) or a,
                     liste_test_hit, collections.Counter()))

    result_total = dict(functools.reduce(lambda a, b: a.update(b) or a,
                     liste_test_total, collections.Counter()))
  
    print("hit sum dico : ", str(result_hit))
    print("total sum dico : ", str(result_total))

    liste_value_right_order = []

    lst = list(itertools.zip_longest(*liste_amp_all))

    for icount in range(len(lst)):
        moy = pstdev(lst[icount])
        liste_value_right_order.append(moy)

    print("right order")
    print(liste_value_right_order)

    for (key1, value1), (key2, value2) in zip (result_hit.items(), result_total.items()):
        info_x_axis.append(float(key1))
        hit_rate_concatenation = value1 / value2
        hit_rate_concatenation = float("{:.2f}".format(hit_rate_concatenation))
        info_concatenation.append(hit_rate_concatenation)

    xdata = np.array(info_x_axis)
    ydata = np.array(info_concatenation)
    print(xdata)
    print(ydata)

    popt, pcov = curve_fit(sigmoid, xdata, ydata, maxfev= 3000) # Scipy defines a value called maxfev, whose purpose is after how many iterations it gives up on the search (we can alter this parameter)
    fix_value = info_x_axis[-1] + 0.1

    x = np.linspace(0, fix_value, 50)
    y = sigmoid(x, *popt)

    x_for_y_0_5 = fsolve(find_x_for_y_0_5, x0=0, args=(popt[0], popt[1]))
    print("")
    print("The value for y=0.5 is : ", x_for_y_0_5[0])
    print("")
    x0, k = popt
    inflection_point = x0
    print("")
    print("The inflection point is : ", inflection_point)
    print("")

    # Generate finer x values within your x-data range
    x_fine = np.linspace(min(xdata), max(xdata), 1000)

    # Compute the first and second derivatives of the fitted curve
    y_fitted = sigmoid(x_fine, *popt)
    dy_dx = np.gradient(y_fitted, x_fine)
    d2y_dx2 = np.gradient(dy_dx, x_fine)

    # Find the inflection point where the second derivative is closest to zero
    inflection_index = np.argmin(np.abs(d2y_dx2))
    inflection_point1 = x_fine[inflection_index]

    print(f"The inflection point is approximately at x = {inflection_point1:.2f}")

    slope_polyfit, intercept_polyfit = np.polyfit(x,y,1)

    slope_linregress, intercept_linregress, r_value, p_value, std_err = linregress(x, y)
    dico_slop = {"Slope with polyfit" : slope_polyfit, "Slope with linregre": slope_polyfit}
    dico_x_for_y_0_5 = {'value_for_y_0_5_concat': float("{:.2f}".format(x_for_y_0_5[0]))}
    dico_inflection_point = {'inflection point': float("{:.2f}".format(inflection_point))}

    big_info = [result_hit, result_total, info_x_axis, info_concatenation, dico_slop, dico_x_for_y_0_5, dico_inflection_point]

    with open(str(dirname) + '/infoPyschoConcatenationOnly.json', 'w') as jsonFile:
        json.dump(big_info, jsonFile, indent=4)

    fig, axs = plt.subplots(1)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)

    axs.set_xlim(0,fix_value)
    axs.set_ylim(0,1)

    axs.axvline(inflection_point, color='green', linestyle='--', label=f'Inflection Point = {inflection_point1:.2f}')

    axs.plot(xdata, ydata, 'o', label='Concatenation')
    axs.plot(x,y,label='fit_WT')

    for icount_ax in range(len(liste_value_right_order)):
        axs.errorbar(xdata[icount_ax], ydata[icount_ax], yerr= liste_value_right_order[icount_ax], fmt='.k')

    #plt.legend()
    plt.tight_layout()
    plt.show()

def weibull_concatenation(myFile_json):
    info_weibull = []

    for icount_json in range(len(myFile_json[0])):
        with open(myFile_json[0][icount_json], "r") as read_file:
            info_json = json.load(read_file)
            info_weibull.append(info_json[2])
    
    print(info_weibull)

    liste_test_hit = []
    liste_test_total = []
    liste_final = []
    info_x_axis = []
    info_concatenation = []

    print(myFile_json)
    for icount in range (len(info_weibull)):
        liste_test_hit.append(info_weibull[icount][0])
        liste_test_total.append(info_weibull[icount][1])

    result_hit = dict(functools.reduce(operator.add,
         map(collections.Counter, liste_test_hit)))

    result_total = dict(functools.reduce(operator.add,
         map(collections.Counter, liste_test_total)))
  
    print("hit sum dico : ", str(result_hit))
    print("total sum dico : ", str(result_total))

    for (key1, value1), (key2, value2) in zip (result_hit.items(), result_total.items()):
        info_x_axis.append(float(key1))
        hit_rate_concatenation = value1 / value2
        hit_rate_concatenation = float("{:.2f}".format(hit_rate_concatenation))
        info_concatenation.append(hit_rate_concatenation)

    print(info_x_axis)
    print(info_concatenation)

    plot_things_weibull(info_concatenation, info_x_axis)
