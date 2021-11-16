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


def get_park_names():

    '''  Queries the database for the names of all 56 National Parks for our drop down selector '''

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



@api.route('/park_search/', strict_slashes=False)
def get_park():
    name = flask.request.args.get('park_name')
    state = flask.request.args.get('state')
    if name == 'selectParkName':
        name = ''
    if state == 'selectState':
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


@api.route('/park_search/parks', strict_slashes=False)
def load_parks():
    return json.dumps(get_park_names())


@api.route('/park_search/states', strict_slashes=False)
def load_states():
    return json.dumps(get_state())


@api.route('/species_search/', strict_slashes=False)
def get_species():
    selectors_arr = [get_park_names(), get_state(), get_category()]
    return json.dumps(selectors_arr)


# @api.route('/species_search/categories', strict_slashes=False)
# def get_species():
#     return json.dumps(get_category())





