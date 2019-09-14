import numpy as np
import matplotlib.pyplot as plt
import pysolr
import json
import csv


query1 = 'Camera does not working with autofocus'
query2 = 'The application is crashing after switching'
relevancia_query1 = 'relevancia1.csv'
relevancia_query2 = 'relevancia2.csv'


def connect_to_solr(core, port=8983):
    solr_instance = pysolr.Solr('http://localhost:{}/solr/{}'.format(port, core), always_commit=True)
    return solr_instance

def search(solr_instance, query, n=100):
    result = solr_instance.search(query, **{'rows'=n})
    return result

def read_csv(csv_file):
    csv_as_list = list()
    with open(csv_file) as csv:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            csv_as_list.append(line)
    return csv_as_list

def is_relevant(result, csv_as_list):
    relevant = False
    for line in csv_as_list:
        if (result['key'] == line[0]):
            if (line[1] == '1'):
                relevant = True
        break
