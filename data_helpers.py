import pandas as pd
import json

# Load data

# read the master genera data file
try:
    infile='data/genera_master.txt'
    with open(infile, 'r') as infile:
        indata = infile.read()
    genera_dict = json.loads(indata)
except FileNotFoundError as fnf_error:
    print(fnf_error)

# read relative interest file
try:
    infile='data/genera_relative_interest.txt'
    with open(infile, 'r') as infile:
        indata = infile.read()
    interest = json.loads(indata)
except FileNotFoundError as fnf_error:
    print(fnf_error)

# read genus-level google shopping summary
try:
    infile='data/gs_genus.txt'
    with open(infile, 'r') as infile:
        gs_genus = pd.read_json(infile, orient='table')
except FileNotFoundError as fnf_error:
    print(fnf_error)

# read genus-level competitor file
try:
    infile='data/gs_genus_comp.txt'
    with open(infile, 'r') as infile:
        gs_genus_comp = pd.read_json(infile, orient='table')
except FileNotFoundError as fnf_error:
    print(fnf_error)

##  Data and functions for use in filters / dropdowns

# get the options for plant types
plant_types = set()
[plant_types.update(v['plant_types']) for k,v in genera_dict.items()]
plant_type_options = [ {'label':e, 'value':e} for e in plant_types ]

# get lookup of genera to display, given selected plant types
def genera_to_show(genera_dict, types):
    type_to_genera = {}
    for g, v in genera_dict.items():
        for t in v['plant_types']:
            if t not in type_to_genera:
                type_to_genera[t] = []
            type_to_genera[t].append(g)

    distinct_genera = set()
    [distinct_genera.update(type_to_genera[t]) for t in types]
    return sorted(distinct_genera)