import numpy as np
import matplotlib.pyplot as plt
import pysolr
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


def write_results(results, query, core):
    with open('{}_{}.txt'.format(query, core), 'a') as file:
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
    write_results(results, query, core)
    print('QUANTIDADE DE RESULTADOS RETORNADOS DA QUERY: {} \n'.format(len(results)))
    for r in results:
        countT += 1
        check = is_relevant(r, r1)
        if check:
            countR += 1
            accuracy.append(round(countR/countT, 2))
            coverage.append(countR)
        print(r['key'] + ' {}'.format(check))
    coverage = [element/countR for element in coverage]
    print('\nRESULTADOS RELEVANTES DA QUERY: {}'.format(countR))
    return accuracy, coverage


def main():
    query1 = 'Camera does not working with autofocus'
    query2 = 'The application is crashing after switching'
    relevancia_query1 = 'relevancia_q1.csv'
    relevancia_query2 = 'relevancia_q2.csv'
    solr = connect_to_solr('bolinha')
    b2 = connect_to_solr('base2')
    b3 = connect_to_solr('base3')
    b4 = connect_to_solr('base4')

    print('\nBASE 01\n')
    print('\n-----Q1-----\n')
    acu_b1q1, cov_b1q1 = analyse_query(solr, query1, relevancia_query1)
    print('\n-----Q2-----\n')
    acu_b1q2, cov_b1q2 = analyse_query(solr, query2, relevancia_query2)

    print('\nBASE 02\n')
    print('\n-----Q1-----\n')
    acu_b2q1, cov_b2q1 = analyse_query(b2, query1, relevancia_query1)
    print('\n-----Q2-----\n')
    acu_b2q2, cov_b2q2 = analyse_query(b2, query2, relevancia_query2)

    print('\nBASE 03\n')
    print('\n-----Q1-----\n')
    acu_b3q1, cov_b3q1 = analyse_query(b3, query1, relevancia_query1)
    print('\n-----Q2-----\n')
    acu_b3q2, cov_b3q2 = analyse_query(b3, query2, relevancia_query2)

    print('\nBASE 04\n')
    print('\n-----Q1-----\n')
    acu_b4q1, cov_b4q1 = analyse_query(b4, query1, relevancia_query1)
    print('\n-----Q2-----\n')
    acu_b4q2, cov_b4q2 = analyse_query(b4, query2, relevancia_query2)

    # plot analysis for query1
    graph1 = plt.figure()
    ax = graph1.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_xlabel('Coverage')
    ax.set_ylabel('Accuracy')
    ax.plot(cov_b1q1, acu_b1q1, 'red', marker='o', label='Base 1')
    ax.plot(cov_b2q1, acu_b2q1, 'blue', marker='o', label='Base 2')
    ax.plot(cov_b3q1, acu_b3q1, 'yellow', marker='o', label='Base 3')
    ax.plot(cov_b4q1, acu_b4q1, 'green', marker='o', label='Base 4')
    ax.legend()

    # plot analysis for query2
    graph2 = plt.figure()
    bx = graph2.add_axes([0.1, 0.1, 0.8, 0.8])
    bx.set_xlabel('Coverage')
    bx.set_ylabel('Accuracy')
    bx.plot(cov_b1q2, acu_b1q2, 'red', marker='o', label='Base 1')
    bx.plot(cov_b2q2, acu_b2q2, 'blue', marker='o', label='Base 2')
    bx.plot(cov_b3q2, acu_b3q2, 'yellow', marker='o', label='Base 3')
    bx.plot(cov_b4q2, acu_b4q2, 'green', marker='o', label='Base 4')
    bx.legend()

    plt.show()

if __name__ == "__main__":
    main()
