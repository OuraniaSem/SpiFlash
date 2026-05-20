import json
from main_function_Sp import catch_info_xls

def save_eventDico_json(the_dico,  directory_name):
    with open(directory_name, 'w') as jsonFile:
        json.dump(the_dico, jsonFile, indent=4)

def main_wrap(ma_path, name_files):
    # get the info from the excell file
    my_data_xls, my_dirname = catch_info_xls(ma_path)

    myFile_json = [str(my_dirname) + "/infoBarplot.json",
                   str(my_dirname) + "/data_event_full.json",
                   str(my_dirname) + "/infoPyscho.json"]

    new_names_file = name_files.split('.')

    path = str(my_dirname) + "/wrap_" + str(new_names_file[0]) + ".json"

    general_info = []
    for icount_json in range(len (myFile_json)):
        print("MyFile_Json is called ", myFile_json[icount_json])

    for icount_json in range(len (myFile_json)):
        with open(myFile_json[icount_json], "r") as read_file:
            info_json = json.load(read_file)
            print(info_json)
            general_info.append(info_json)

    save_eventDico_json(general_info, path)


def main_wrap_2afc(ma_path, name_files):
    # get the info from the excell file
    my_data_xls, my_dirname = catch_info_xls(ma_path)

    myFile_json = [str(my_dirname) + "/infoBarplot.json",
                   str(my_dirname) + "/data_event_full.json",
                   str(my_dirname) + "/infoPyscho.json",
                   str(my_dirname) + "/infoPriors.json"]

    new_names_file = name_files.split('.')

    path = str(my_dirname) + "/wrap_2afc" + str(new_names_file[0]) + ".json"

    general_info = []
    for icount_json in range(len (myFile_json)):
        print("MyFile_Json is called ", myFile_json[icount_json])

    for icount_json in range(len (myFile_json)):
        with open(myFile_json[icount_json], "r") as read_file:
            info_json = json.load(read_file)
            print(info_json)
            general_info.append(info_json)

    save_eventDico_json(general_info, path)