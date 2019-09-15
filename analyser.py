import numpy as np
import matplotlib.pyplot as plt
import pysolr
import json
import csv


def connect_to_solr(core, port=8983):
    solr_instance = pysolr.Solr('http://localhost:{}/solr/{}'.format(port, core), always_commit=True)
    return solr_instance


def search(solr_instance, query, n=100):
    result = solr_instance.search(query, **{'rows': n})
    return result


def read_csv(csv_file):
    csv_as_list = list()
    with open(csv_file) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            csv_as_list.append(line)
    return csv_as_list


def write_results(results, query):
    with open('{}.txt'.format(query), 'a') as file:
        file.truncate(0)
        for result in results:
            file.write('KEY: ' + result['key'] + '\n')
            file.write('SUMMARY: ' + result['summary'] + '\n')
            file.write('DESCRIPTION: ' + result['description'] + '\n')
            file.write('\n\n')


def is_relevant(result, csv_as_list):
    relevant = False
    for line in csv_as_list:
        if (result['key'] == line[0]):
            if (line[1] == '1'):
                relevant = True
            break
    return relevant


def analyse_query(core, query, matriz_relevancia):
    countR, countT = 0, 0
    accuracy = list()
    coverage = list()
    r1 = read_csv(matriz_relevancia)
    results = search(core, query)
    write_results(results, query)
    print('QUANTIDADE DE RESULTADOS RETORNADOS DA QUERY: {} \n'.format(len(results)))
    for r in results:
        countT += 1
        check = is_relevant(r, r1)
        if check:
            countR += 1
            accuracy.append(countR/countT)
            accuracy.append(countR)
        print(r['key'] + ' {}'.format(check))
    coverage_q1 =  [element/countR for element in coverage]
    print('\nRESULTADOS RELEVANTES DA QUERY: {}'.format(countR))


def main():
    query1 = 'Camera does not working with autofocus'
    query2 = 'The application is crashing after switching'
    relevancia_query1 = 'relevancia_q1.csv'
    relevancia_query2 = 'relevancia_q2.csv'
    solr = connect_to_solr('bolinha')

    print('\n-----Q1-----\n')
    analyse_query(solr, query1, relevancia_query1)

    print('\n-----Q2-----\n')
    analyse_query(solr, query2, relevancia_query2)

if __name__ == "__main__":
    main()
