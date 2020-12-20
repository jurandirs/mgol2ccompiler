#!/usr/bin/env python
import csv
import sys
import pprint

#class Dicionario:


# Function to write the diferents id's;
def csv_write(file, token, lexema, tipo):
     
    fieldnames = ["token", "lexema", "tipo"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow([token, lexema, tipo])
 

#return the token definition whith lexema, token and type
def token_definition(list1, list2, token, lexema, tipo):
    return 1

# Função que lê um arquivo CSV e organiza cada linha como um dicionário
# class_name poderá ser Reserved, ID, ou Data (denotando qualquer coisa, caso seja preciso)
def csv_dict_list(file_name, class_name="Data"):
    # Function to convert a csv file to a list of dictionaries.
    with open(file_name, 'r') as F:
        reader = csv.reader(F)
        fields = next(reader)
        data_list = [dict(list(zip(fields,r))+[('Class',class_name)]) for r in reader]
    return data_list

def read_csv(file_name):
    with open(file_name)as F:
        reader = csv.reader(F)
        fields = next(reader)
        rows = [line for line in reader]
    return fields, rows