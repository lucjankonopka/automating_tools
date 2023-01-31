#!/clients/bin/python
#

import os
from os.path import exists
import time
from datetime import datetime

###################################################################################################################
# Python code
###################################################################################################################

start = time.time()

# Creating the timestamp
Timestamp = datetime.now()
fileNameTimestamp_str = Timestamp.strftime('%Y%m%d_%H%M%S')


###################################################################################################################
# PAM DEFINITION
###################################################################################################################

# Elements tuples:
NODE = ("NODE  / 740", "NODE  / 741")
MEMBR = ("MEMBR / 740", "MEMBR / 741")
BAR = ("BAR   / 740", "BAR   / 741")
SHELL = ("SHELL / 740", "SHELL / 741")

ELE_LIST = ("MEMBR /", "SHELL /", "BAR   /")

CLOSING_SHELLS = ("$ Closing", "$ closing", "$Closing", "$closing")
DIFFUSOR = ("$ Diffusor", "$ diffusor", "$Diffusor", "$diffusor")


###################################################################################################################
# INPUTS VALIDATION FUNCTIONS
###################################################################################################################
ERROR_TEXT = "\nThis is not a correct input. Type again.\n"

def base_include_check():
    while True:
        print('Insert the base include file:')
        base_include_file = input(">>>")
        if not base_include_file.endswith(".inc"):
            print(ERROR_TEXT)
            continue
        else: break        
    return base_include_file

def base_metric_check():
    while True:
        print('Insert the base metric file:')
        base_metric_file = input(">>>")
        if not base_metric_file.endswith(".mtr"):
            print(ERROR_TEXT)
            continue
        else: break
    return base_metric_file          
    
def new_shape_check():
    while True:
        print('Insert the new shape include file:')
        new_shape_file = input(">>>")
        if not new_shape_file.endswith(".inc") and not new_shape_file.endswith(".pc"):
            print(ERROR_TEXT)
            continue
        else: break
    return new_shape_file

#def closing_shells_check():
#    while True:
#        print('Is closing shells part already defined? y/Y or n/N')
#        cs_answer = input(">>>")
#        if cs_answer == "y" or cs_answer == "Y":
#            while True:
#                print("Part number of closing shells:")
#                cs_part = input(">>>")
#                if not cs_part.isdigit():
#                    print(ERROR_TEXT)
#                    continue
#                else: break
#            break
#        elif cs_answer == "n" or cs_answer == "N":
#            break
#        else:
#            print("Wrong input! Try again")
#            continue
#    return cs_part

###################################################################################################################
# INPUTS CHECK FUNCTIONS
###################################################################################################################

# Checking the amount of nodes in files to compare models
# They amount of nodes has to be the same to change elements correctly
def check_inputs(base_file, new_shape_file):
    with open(base_file , 'r') as input:
        text = input.readlines()
        counter_base = 0
        for new_line in text:
            if new_line.startswith(NODE) and int(new_line[8:16]) in range(74000000, 74169999):
                counter_base += 1
  
    with open(new_shape_file , 'r') as input:
        text = input.readlines()
        counter_new = 0
        for new_line in text:
            if new_line.startswith(NODE) and int(new_line[8:16]) in range(74000000, 74169999):
                counter_new += 1
    
# Checking equality of the nodes:
    if counter_base != counter_new:
        print("""\nNew shape has different amount of nodes than basis shape!
Please check the input files and try again.\n""")
        return False


###################################################################################################################
# NEW ELEMENTS LIST FUNCTIONS
###################################################################################################################                
	
# Looking for elements to copy from new file
# List of all elements for include:
list_new_elements = []

def find_new_elements():
    with open(new_shape_file , 'r') as input:
        text = input.readlines()
        for new_line in text:
            if new_line.startswith(MEMBR) and int(new_line[8:16]) in range(74000000, 74169999):
                list_new_elements.append(new_line)
            elif new_line.startswith(BAR) and int(new_line[8:16]) in range(74000000, 74169999):
                list_new_elements.append(new_line)
            elif new_line.startswith(SHELL) and int(new_line[17:24]) not in range(7400400, 7400499):
                list_new_elements.append(new_line)
            else:
                continue
    return list_new_elements

###################################################################################################################
# NODES LIST FUNCTIONS
###################################################################################################################                
	
# Looking for elements to copy from new file
# List of cushion nodes for include:
list_cushion_inc_nodes = []
# List of cushion nodes for metric:
list_cushion_mtr_nodes = []

def find_nodes_inc():
    with open(base_include_file , 'r') as input:
        text = input.readlines()
        for new_line in text:
            if new_line.startswith(NODE) and int(new_line[8:16]) in range(74000000, 74169999):
                list_cushion_inc_nodes.append(new_line)
            else:
                continue
    return list_cushion_inc_nodes 


def find_nodes_mtr():
    with open(base_metric_file , 'r') as input:
        text = input.readlines()
        for new_line in text:
            if new_line.startswith(NODE) and int(new_line[8:16]) in range(74000000, 74169999):
                list_cushion_mtr_nodes.append(new_line)
            else:
                continue
    return list_cushion_mtr_nodes        

###################################################################################################################
# DEAD CUSHION FUNCTIONS
###################################################################################################################

# Checking if dead cushion parts/elements have to be deleted
def dead_cushion():
    while True:
        print('Do you want to delete "dead cushion"? y/Y or n/N?')
        dc_answer = input(">>>")
        if dc_answer == "y" or dc_answer == "Y":
            while True:
                print("How many parts are to delete?")
                dc_parts = input(">>>")
                if not dc_parts.isdigit():
                    print(ERROR_TEXT)
                    continue
                if int(dc_parts) > 10:
                    print("\nThat seems to be a wrong input. Read the question again.\n")
                    continue
                else:
                    break
            dead_cushion_selector(dc_parts)
            break
        elif dc_answer == "n" or dc_answer == "N":
            print("No deletion needed.")
            break
        else:
            print(ERROR_TEXT)
            continue

# Selecting and deleting dead cushion parts/elements if exists
def dead_cushion_selector(dc_parts):
    dc_parts_list = []
    global list_new_elements
    i = 0
    while i < int(dc_parts):
        sel_part = input("Part number to be deleted: ")
        if not sel_part.isdigit():
            print("\nThis is not a valid part number. Type again\n")
            continue
        # Deleting elements in include list:
        list_without_dc_parts = [el for el in list_new_elements if el[17:24] != sel_part]
        if list_new_elements == list_without_dc_parts:
            print("\nThis part do not exist! Please check the input.\n")
            continue
        else:
            i += 1
            list_new_elements = list_without_dc_parts
    print("-"*64)
    print("""\n Dead cushion elements deleted. 
!!! Be sure to use freenod.pl to delete the free nodes !!!\n""")

###################################################################################################################
# NEW LINES LISTS
###################################################################################################################	     

include_nodes_list = []
metric_nodes_list = []

###################################################################################################################
# MAIN PROGRAM CODE
###################################################################################################################


# Inserting the names of input files:
print("-"*64)

while True:

    base_include_file = base_include_check()
    dot = base_include_file.rfind('.')
    print(base_include_file)
    base_metric_file = base_metric_check()
    new_shape_file = new_shape_check()

    #closing_shells = closing_shells_check()


    check_incl = check_inputs(base_include_file, new_shape_file)
    check_mtr = check_inputs(base_metric_file, new_shape_file)
    
    if check_incl == False or check_incl == False:
        break
    
    find_new_elements()
    find_nodes_inc()
    find_nodes_mtr()
    dead_cushion()
    
    output_include_file = base_include_file[:dot]+"_"+fileNameTimestamp_str+base_include_file[dot:]
    output_metric_file = base_metric_file[:dot]+"_"+fileNameTimestamp_str+base_metric_file[dot:]
    print("-"*64)


    # Checking the data existance/creating backup file:
    if os.path.exists(output_include_file + '.old') == True:
        os.remove(output_include_file + '.old')
    if os.path.exists(output_include_file) == True:
        os.rename(output_include_file, output_include_file + '.old')
   
    
    if os.path.exists(output_metric_file + '.old') == True:
        os.remove(output_metric_file + '.old')   
    if os.path.exists(output_metric_file) == True:
        os.rename(output_metric_file, output_metric_file + '.old')

    
    # Saving an include with new shape:
    with open(base_include_file , 'r') as include_input, open(output_include_file, 'w') as output_inc:
        text = include_input.readlines()
        for new_line in text:
            if new_line.startswith("NODE  / 74000001"):
                for el in list_cushion_inc_nodes:
                    output_inc.write(el)
                for el in list_new_elements:
                    output_inc.write(el)      
            if new_line.startswith(NODE) and int(new_line[8:16]) in range(74000000, 74169999):
                continue
            if new_line.startswith(ELE_LIST) and int(new_line[17:24]) in range(7400100, 7400599):
                if int(new_line[17:24]) not in range(7400400, 7400499):
                    continue
            output_inc.write(new_line)


    # Saving a metric with new shape:
    list_new_membranes = [el for el in list_new_elements if el.startswith(MEMBR)]
    with open(base_metric_file , 'r') as metric_input, open(output_metric_file, 'w') as output_mtr:
        text = metric_input.readlines()
        for new_line in text:
            if new_line.startswith("NODE  / 74000001"):
                for el in list_cushion_mtr_nodes:
                    output_mtr.write(el)
                for el in list_new_membranes:
                    output_mtr.write(el)     
            if new_line.startswith(NODE) and int(new_line[8:16]) in range(74000000, 74169999):
                continue
            if new_line.startswith(MEMBR) and int(new_line[8:16]) in range(74000000, 74169999):
                continue
            output_mtr.write(new_line)


    print("-"*64)
    print("\nElements exchange done!\n")
    print("-"*64)
    break

###################################################################################################################
# WORK TIME CHECK
###################################################################################################################

# Work-time:
end = time.time()
time = str(end - start)
print("Elapsed time: {0}s\n".format(time))


#
# Tool to exchange shape in include and metric files
# in Pam-Crash HSAB models
#
# pam-crash
# author: konopkal <Lucjan Konopka>
# contact: lucjan.konopka@joysonsafety.com
# organization: JSS Berlin CAE
#
