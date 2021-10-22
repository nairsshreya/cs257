'''
    Author : Shreya Nair
    CS 257 Fall 2021

    Program that serves as an interface between the database and command line. Accepts 3 requests.
    For olympic data.
'''
from config import user
from config import password
from config import database

import psycopg2
import sys


try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()


def list_athlete_from_noc(noc_name):

    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    search_string = noc_name
    query = '''SELECT DISTINCT athletes.name 
                FROM athletes, athlete_medal, noc 
                WHERE athletes.id = athlete_medal.athlete_id
                AND noc.noc_id = athlete_medal.noc_id 
                AND noc.noc_id = %s;
                 '''
    try:
        cursor.execute(query, (search_string,))
    except Exception as e:
        print(e)
        exit()
    return cursor


def print_athlete_noc(results, search_string):
    print('===== Athletes from NOC :  {0} ====='.format(search_string))
    for athlete in results:
        print(athlete)
    print()


def gold_medal_num():
    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    query = '''SELECT COUNT (athlete_medal.medal), athlete_medal.noc_id
                FROM athlete_medal, noc
                WHERE noc.noc_id = athlete_medal.noc_id
                AND athlete_medal.medal = 'Gold'
                GROUP BY athlete_medal.noc_id
                ORDER BY COUNT(athlete_medal.medal) DESC;
                '''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    return cursor


def list_all_events_and_sport():
    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    query = '''SELECT event.event_name FROM event;
                '''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    return cursor

def athlete_events(athlete_name):

    search_string = '%' + athlete_name + '%'
    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    query = ''' SELECT DISTINCT athletes.name,event.event_name, games.game_name, noc.region
                FROM athletes, athlete_medal, event, games, noc
                WHERE athletes.id = athlete_medal.athlete_id
                AND noc.noc_id = athlete_medal.noc_id
                AND event.event_id = athlete_medal.event_id
                AND games.game_id = athlete_medal.game_id
                AND athletes.name ILIKE %s '''

    try:
        cursor.execute(query, (search_string,))
    except Exception as e:
        print(e)
        exit()
    return cursor


def display_noc_medals(results):
    print('===== NOCs Gold Medal List =====')
    print()
    print(f'{"NOC".center(3):5} {"Number of Gold".center(10):5} ')
    print('-' * 20)
    for event in results:
        print(f'{event[1]:5} {event[0]:5} ')
    print()


def display_events(results):
    print('===== Events List  =====')
    for event in results:
        print(event[0])
    print()


def display_noc_athletes(results, search):

    print('===== Athletes from {0} ====='.format(search))
    for athlete in results:
        print(athlete[0])
    print()


def display_athlete_events(results):
    print('===== Athlete Event List =====')
    print(f'{"Name".center(25):50} {"Event".center(30):50} {"Games".center(10):15} {"NOC".center(3):10}')
    print('-' * 125)
    for event in results:
        print(f'{event[0]:50} {event[1]:50} {event[2]:15} {event[3]:10}')
    print()


def help_txt():
    log = open("usage.txt", "r").read()
    print(log)
    sys.exit()


def check_empty_result(results):

    if results.rowcount == 0:
        print("Sorry, nothing came up with your search, please try again.")
        return True

    else:
        return False


if len(sys.argv) < 2:
    print("Require a command for program, please try again")
else :
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        help_txt()

    # Command for search : Athlete names from specified NOC
    if sys.argv[1] == "-lan" or sys.argv[1] == "--listathletenoc":
        if len(sys.argv) == 3:
            search = sys.argv[2].upper()
            results = list_athlete_from_noc(search)
            if not check_empty_result(results):
                display_noc_athletes(results, search)
        else:
            print("Wrong syntax, requires an NOC search string,  check usages by running with -h or --help.")

    if sys.argv[1] == "-lng" or sys.argv[1] == "--listnocgold":
        results = gold_medal_num()
        if not check_empty_result(results):
            display_noc_medals(results)

    if sys.argv[1] == "-ae" or sys.argv[1] == "--athleteevent":
        if len(sys.argv) == 3:
            results = athlete_events(sys.argv[2])
            if not check_empty_result(results):
                display_athlete_events(results)

        else:
            print("Wrong syntax, requires an athlete's name, check usages by running with -h or --help.")
    
    if sys.argv[1] == "-e" or sys.argv[1] == '--events':
        results = list_all_events_and_sport()
        if not check_empty_result(results):
            display_events(results)

connection.close()
