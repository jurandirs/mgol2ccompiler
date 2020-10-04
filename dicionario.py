#!/usr/bin/env python
 
import csv
import sys
import pprint

# Function to write the diferents id's;

def csv_write(file, token, lexema, tipo):
     
    fieldnames = ["token", "lexema", "tipo"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow([token, lexema, tipo])
 
def csv_dict_list(variables_file):
     
    # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs
 
    reader = csv.DictReader(open(variables_file, 'rb'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list

# Function to convert a csv file to a list of dictionaries.  Takes in one variable called &quot;variables_file&quot;
 
def csv_dict_list(variables_file):
     
    # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs
 
    reader = csv.DictReader(open(variables_file, 'rb'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list
 
# Calls the csv_dict_list function, passing the named csv
 
simbolo_values = csv_dict_list("tabSimbolos.csv")
 
# Prints the results nice and pretty like
 
pprint.pprint(simbolo_values)

# Calls the csv_dict_list function, passing the named csv
 
estfinais_values = csv_dict_list("tabEstadosFinais.csv")
 
# Prints the results nice and pretty like
 
pprint.pprint(estfinais_values)
        