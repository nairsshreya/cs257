'''
    api.py
    Shreya Nair and Elliot Hanson, 5th November 2021
    Updated 15th November 2021

    Flask API to support a national parks web application that connects to a database and uses user input to
    format queries and display results.
'''
import flask
import json
import psycopg2
import config
import sys

api = flask.Blueprint('api', __name__)


def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.username,
                            password=config.password)


def get_state():

    '''  Queries the database for the names and id of all 50 American states for our drop down selector '''

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


def get_park_info():

    '''  Queries the database for the names of all 56 National Parks for our drop down selector '''

    query = '''SELECT park_code, park_name, state_code, acreage, longitude, latitude
                       FROM parks ORDER BY park_name'''
    park_names = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            park_info = {'park_code': row[0], 'park_name': row[1], 'state_code': row[2], 'acreage': row[3], 'longitude': row[4],
                         'latitude': row[5]}
            park_names.append(park_info)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return park_names


def get_category():
    '''  Queries the database for the names of 14 categories of species for our drop down selector '''
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


# TODO Not sure what this is but might break code ? hopefully not will remove before final turn in.
# def park_search_state():
#
#     query = '''SELECT park_name
#                           FROM parks, states WHERE state.id = park.state_id ORDER BY park_name'''
#     categories = []
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#         cursor.execute(query, tuple())
#         for row in cursor:
#             category = {'name': row[0]}
#             categories.append(category)
#         cursor.close()
#         connection.close()
#     except Exception as e:
#         print(e, file=sys.stderr)
#     return categories


@api.route('/park_search/parks', strict_slashes=False)
def load_parks():
    ''' Loads the information for our parks selector and returns data to the javascript file. '''
    return json.dumps(get_park_info())


@api.route('/park_search/states', strict_slashes=False)
def load_states():
    ''' Loads the information for our states selector and returns data to the javascript file. '''
    return json.dumps(get_state())


@api.route('/park_search/', strict_slashes=False)
def get_park():
    '''Queries the database for the park(s) information based on selected values from the user.
        Handles exceptions when park names and/or state names are not selected.
    '''
    name = flask.request.args.get('park_name')
    state = flask.request.args.get('state')
    if name == 'selectParkName' or name is None :
        name = ''
    if state == 'selectState' or state is None:
        state = ''
    
    name = '%' + name + '%'
    state = '%' + state + '%'
    
    query = '''SELECT park_code, park_name, state_code, acreage, longitude, latitude
                               FROM parks, states
                               WHERE parks.park_name LIKE %s
                               AND parks.state_code = states.id
                               AND parks.state_code LIKE %s
                               ORDER BY park_name'''
    park_results = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (name, state))

        for row in cursor:
            park = {'park_code': row[0], 'park_name': row[1], 'state_code': row[2],
                    'acreage': row[3], 'longitude': row[4], 'latitude': row[5]}
            print(row)
            park_results.append(park)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    
    return json.dumps(park_results)



# Code for Species Page
@api.route('/species_search/', strict_slashes=False)
def get_species():
    ''' Loads the information for our selectors for species page and returns data to the javascript file.
        NEEDS WORK, UPDATES TO STRUCTURE but can run so page will load but not return results yet.'''
    selectors_arr = [get_park_info(), get_state(), get_category()]
    return json.dumps(selectors_arr)


# @api.route('/species_search/categories', strict_slashes=False)
# def get_species():
#     return json.dumps(get_category())





