'''
    app.py
    Shreya Nair and Elliot Hanson, 25 April 2016
    Updated 5 November 2021

    Tiny Flask API to support a cats and dogs web application
    that doesn't use a database.
'''
import flask
import json
import psycopg2
import config
import sys

api = flask.Blueprint('api', __name__)

# # Of course, your API will be extracting data from your postgresql database.
# # To keep the structure of this tiny API crystal-clear, I'm just hard-coding data here.
cats = [{'name':'Emma', 'birth_year':1983, 'death_year':2003, 'description':'the boss'},
        {'name':'Aleph', 'birth_year':1984, 'death_year':2002, 'description':'sweet and cranky'},
        {'name':'Curby', 'birth_year':1999, 'death_year':2000, 'description':'gone too soon'},
        {'name':'Digby', 'birth_year':2000, 'death_year':2018, 'description':'the epitome of Cat'},
        {'name':'Max', 'birth_year':1998, 'death_year':2009, 'description':'seismic'},
        {'name':'Scout', 'birth_year':2007, 'death_year':None, 'description':'accident-prone'}]

dogs = [{'name':'Ruby', 'birth_year':2003, 'death_year':2016, 'description':'a very good dog'},
        {'name':'Maisie', 'birth_year':2017, 'death_year':None, 'description':'a very good dog'}]
#
# states = [{'id':'CA', 'name':'California'}]


def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.username,
                            password=config.password)


def get_state():

    query = '''SELECT id, name
                   FROM states ORDER BY id'''
    states = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            state = {'id': row[0], 'name': row[1]}
            states.append(state)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return states


def get_park_names():
    query = '''SELECT park_code, park_name, state_code, acreage, longitude, latitude
                       FROM parks ORDER BY park_name'''
    park_names = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            park_info = {'park_code': row[0], 'name':row[1], 'state_code':row[2], 'acreage':row[3], 'longitude':row[4],
                         'latitude':row[5]}
            park_names.append(park_info)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return park_names

def get_category():
    query = '''SELECT category
                       FROM categories ORDER BY category'''
    categories = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            category = {'name': row[0]}
            categories.append(category)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return categories

def park_search_state():
    query = '''SELECT park_name
                          FROM parks, states WHERE state.id = park.state_id ORDER BY park_name'''
    categories = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            category = {'name': row[0]}
            categories.append(category)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return categories

@api.route('/park_search', strict_slashes=False)
def get_park():
    selectors_arr = [get_park_names(), get_state()]
    return json.dumps(selectors_arr)

@api.route('/species_search', strict_slashes=False)
def get_species():
    selectors_arr = [get_park_names(), get_state(), get_category()]
    return json.dumps(selectors_arr)


