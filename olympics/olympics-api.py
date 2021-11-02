'''
    Author : Shreya Nair
    API Project for Olympics Database
    Takes requests using the flask app route in browser and returns list of dictionaries containing results.
'''

import sys
import argparse
import flask
import json
import psycopg2
from config import user
from config import password
from config import database

debug = False
app = flask.Flask(__name__)
try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()


@app.route('/games')
def get_games():
    '''
        uses the route /games to get a list of all the unique olympic games held, sorted by year.
    '''
    games_list = []
    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    query = '''SELECT DISTINCT game_id, year, season, city
                   FROM games
                   WHERE games.game_id = game_id
                   ORDER BY year;
                    '''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    for item in cursor:
        if debug:
            print(item)
        game = [{"id": item[0]}, {"year": item[1]}, {"season": item[2]}, {"city": item[3]}]
        # game_dict = {item[0]: [item[1], item[2], item[3]], }
        games_list.append(game)
        # games_list.append(item)
        print(game)
    return json.dumps(games_list)


@app.route('/nocs')
def get_nocs():
    '''
        Uses the route /nocs to display a list of nocs with their id and full name.
    '''
    noc_list = []
    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    query = '''SELECT noc_id, region 
                   FROM noc
                   WHERE noc.noc_id = noc_id
                   ORDER BY noc_id;
                    '''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    for item in cursor:
        if debug:
            print(item)

        noc = [{"id" : item[0]}, {"region": item[1]}]
        noc_list.append(noc)
    return json.dumps(noc_list)


@app.route('/medalists/games/<games_id>')
def get_athlete_medal_in_games(games_id):
    '''
        uses the route /medalists/games/<games_id> to get a list of all the medalists from a specific olympic games,
        if the noc is given then the list contains only medalists from that noc.
    '''
    results_list = []
    noc = flask.request.args.get('noc')
    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()
    if noc is None:

        query = '''SELECT athletes.id, athletes.name, athletes.sex,sports.sport_name, event.event_name, athlete_medal.medal
                    FROM athletes, athlete_medal, event,games, sports
                    WHERE athletes.id = athlete_medal.athlete_id
                    AND event.event_id = athlete_medal.event_id
                    AND event.sport_id = sports.sport_id
                    AND games.game_id = athlete_medal.game_id
                    AND games.game_id = %s
                    AND (athlete_medal.medal = 'Gold' OR athlete_medal.medal = 'Silver' OR athlete_medal.medal = 'Bronze');
                '''
        try:
            cursor.execute(query, (games_id,))
        except Exception as e:
            print(e)
            exit()

    else:

        query = '''SELECT athletes.id, athletes.name, athletes.sex,sports.sport_name, event.event_name, athlete_medal.medal
                            FROM athletes, athlete_medal, event,games, sports, noc
                            WHERE athletes.id = athlete_medal.athlete_id
                            AND athlete_medal.game_id = %s
                            AND athlete_medal.noc_id = %s
                            AND event.event_id = athlete_medal.event_id
                            AND event.sport_id = sports.sport_id
                            AND games.game_id = athlete_medal.game_id
                            AND (athlete_medal.medal = 'Gold' OR athlete_medal.medal = 'Silver' OR athlete_medal.medal = 'Bronze')
                            AND athlete_medal.noc_id = noc.noc_id;

                        '''
        try:
            cursor.execute(query, (games_id,noc))
        except Exception as e:
            print(e)
            exit()

    for item in cursor:
        if debug:
            print(item)
        result_dict = [{"athlete_id": item[0]}, {"athlete_name": item[1]}, {"athlete_sex": item[2]}, {"sport": item[3]},
                       {"event": item[4]}, {"medal": item[5]}]
        results_list.append(result_dict)
    return json.dumps(results_list)

@app.route('/help')
def get_help():
    help_statement = " This is an api to search up olympic data. \n Use /games to get a list of all games held. " \
                     "\n Use /noc to get a list of all nocs in the olympics. \n " \
                     "Use /medalists/games/<game_id>?[noc=noc_abbreviation] for searching up all athletes" \
                     " who won medals in a specific games or further specify those from a particcular noc" \

    return help_statement


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

connection.close()


