"""This script file is for parsing logs from ESP Home addon, 
    and to split one common log to separate CSV files by modules, 
    extract value and unit from each line of log.
    """

import re
from os.path import exists as file_exists
import csv 
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
            short = part[1:]
            info_list.append(short)

        ret_dict['time'] = info_list[0]
        ret_dict['class'] = info_list[1]
        ret_dict['module'] = info_list[2]
        ret_dict['message'] = info_list[3].strip()

    return ret_dict

def message_pars(message, module):
    """Extract unit and value from message row
    return dict with:
    name - sensor name
    text - message text
    value - sensor extracted value
    unit - sensor Unit of Measurement, extaced from row, is none - set to 'raw'
    #
    Now can parse and extact data from 'sensor', 'hx711' and 'ads1115' moduls.
    """
    ret_dict = {} #dict()
    if "':" in message:
        message_list = message.split("':")
        dirty_name = message_list[0] # 'TDS Sensor
        ret_dict['name']= dirty_name[1:] # discard first char
        ret_dict['text']= message_list[1]
    else:
        return ret_dict

    if module=='sensor': #parse " Sending state 6.77216 Ph with 2 decimals of accuracy" text
        split_list = ret_dict.get('text').split(" ")
        ret_dict['value']=split_list[3]
        ret_dict['unit']=split_list[4]

    if module=='hx711': #parse " Got value 556879" text
        split_list = ret_dict.get('text').split(" ")
        ret_dict['value']=split_list[3]
        ret_dict['unit']='raw'

    if module=='ads1115': #parse " Got Voltage=2.047937V" text
        split_list = ret_dict.get('text').split("=")
        dirty_value = split_list[1] # '2.047937V'
        ret_dict['value']=dirty_value[:-1] # '2.047937' - discard last char
        ret_dict['unit']='V'

    return ret_dict

def write_CSV_row(common_dict, writer):
    """
    Function to write value in single CSV file
    Headers already writed
    header = ['Time', 'Module', 'Class', 'Name', 'Value', 'Unit']
    """
    time    = common_dict.get('time')
    module  = common_dict.get('module')
    clas    = common_dict.get('class')
    name    = common_dict.get('name')
    value   = common_dict.get('value')
    unit    = common_dict.get('unit')

    row = [time, module, clas, name, value, unit]
    writer.writerow(row)



def main():
    'main function'
    log = init()
    module_list = []
    files_dict = {}
    for row in log:
        vals_dict = parse_row(row)
        if len(vals_dict) == 0: #skip empty dict
            continue
        time = vals_dict.get('time')
        mod = (vals_dict.get('module').split(":"))[0]
        mess = vals_dict.get('message')
        data_dict = message_pars(mess, mod)
        if len(data_dict) == 0: 
            continue #skip empty dict
        name = data_dict.get('name')
        val = data_dict.get('value')
        unit = data_dict.get('unit')
        print(F'{time} => {mod} => {name} => {val} {unit}')

        common_dict = {**vals_dict, **data_dict}
        header = ['Time', 'Module', 'Class', 'Name', 'Value', 'Unit']
        if mod not in module_list:
            module_list.append(mod)
            print("Make new SCV file for this module")
            file_name = mod + ".csv"
            file_desc = open(file_name,'w', newline="\n")     # 1. create and open a text file
            csvwriter = csv.writer(file_desc, delimiter=';')  # 2. create a csvwriter object
            csvwriter.writerow(header)                        # 3. write the header
            files_dict[mod] = csvwriter                       # 4. save csvwriter object
            
            print(F'Got new module {time} => {mod} => {name} => {val}')

        #add one row with curent value to csv file with  csvwriter object from files_dict
        csvwriter = files_dict.get(mod)
        write_CSV_row(common_dict, csvwriter)

    print(F"All Modules are: {module_list}")
        

main()
