"""This file is for blah blah blah """

import re
from os.path import exists as file_exists
import argparse

def init():
    """ Funcrion init - pars script arguments """
    empty_list = list()
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName", help="log file name to parse")
    args = parser.parse_args()
    file_name = args.fileName
    print(F"ok, try to pars a log: {file_name}")
    if not file_exists(file_name):
        print(F"Error, can't pars a log: {file_name}, file dose not exist.")
        return empty_list

    file_obj = open(file_name, 'r', encoding='utf-8')
    return file_obj


def parse_row(line):
    """row parser - extract info from row like
    [10:26:50][D][hx711:031]: 'HX711 Value': Got value 557038
    and
    [10:26:52][D][sensor:125]: 'PH Sensor': Sending state 6.77072 Ph with 2 decimals of accuracy
    return a dictinary with 'time', 'class', 'module' and 'message' from input row
    """
    pattern = r'\]'
    ret_dict = {} #dict()
    if "]:" in line:
        parts = re.split(pattern, line)
        # now row is split from
        # [10:26:17][C][ads1115:077]:     Unit of Measurement: 'Ph'
        # to list:
        # ['[10:26:17', '[C', '[ads1115:077', ":     Unit of Measurement: 'Ph'\n"]

        # remove first character from parts
        # ['[10:26:17', '[C', '[ads1115:077', ":     Unit of Measurement: 'Ph'\n"]
        # ['10:26:17', 'C', 'ads1115:077', "     Unit of Measurement: 'Ph'\n"]
        info_list = [] #list()
        for part in parts:
            short=part[1:]
            info_list.append(short)

        ret_dict['time']=info_list[0]
        ret_dict['class']=info_list[1]
        ret_dict['module']=info_list[2]
        ret_dict['message']=info_list[3].strip()

    return ret_dict

def main():
    'main function'
    log = init()
    module_list = []
    for row in log:
        vals_dict = parse_row(row)
        if len(vals_dict) == 0: #skip empty dict
            continue
        time = vals_dict.get('time')
        mod = (vals_dict.get('module').split(":"))[0]
        mess = vals_dict.get('message')
        if mod not in module_list:
            module_list.append(mod)
            print(F'Got new module {time} => {mod} => {mess}')
    print(F"All Modules are: {module_list}")

main()
