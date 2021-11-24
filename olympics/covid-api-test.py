'''
    api-test.py
    Jeff Ondich, 11 April 2016
    Updated 7 October 2020
    An example for CS 257 Software Design. How to retrieve results
    from an HTTP-based API, parse the results (JSON in this case),
    and manage the potential errors.
'''

import sys
import json
import urllib.request




def get_cases_and_deaths_state(state):

    url = f' https://api.covidtracking.com/v1/states/{state}/current.json'
    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    stats = json.loads(string_from_server)
    print(stats)
    result_list = []
    cases = stats.get('positive')
    deaths = stats.get('death')
    result_list.append({'cases': cases, 'deaths': deaths})
    return result_list


def jeff_method(state):

    url = f'https://api.covidtracking.com/v1/states/ca/daily.json'
    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    covid_day_list = json.loads(string_from_server)

def main(args):
    if args[1] == "-cad":
        results = get_cases_and_deaths_state(args[2])
        for value in results:
            cases = value['cases']
            deaths = value['deaths']
            print("Number of cases :  ", cases, " Number of deaths : ",deaths)


if __name__ == '__main__':

    main(sys.argv)
