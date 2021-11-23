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
                            user=config.user,
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
        AND parks.state_code LIKE CONCAT('%',states.id,'%')
    '''
    name = flask.request.args.get('park_name')
    state = flask.request.args.get('state')
    if name == 'selectParkName' or name is None :
        name = ''
    if state == 'selectState' or state is None:
        state = ''
    
    name = '%' + name + '%'
    state = '%' + state + '%'
    print(name, state)
    
    query = '''SELECT DISTINCT park_code, park_name, state_code, acreage, longitude, latitude
                               FROM parks, states
                               WHERE parks.park_name LIKE %s
                               AND parks.state_code LIKE %s
                               ORDER BY park_name'''
    park_results = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (name, state))

        for row in cursor:
            print(row)
            park = {'park_code': row[0], 'park_name': row[1], 'state_code': row[2],
                    'acreage': row[3], 'longitude': row[4], 'latitude': row[5]}
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
    
    species_name = flask.request.args.get('name')
    if species_name == 'species_name' or species_name is None:
        species_name = ''
    species_name = '%' + species_name + '%'
    
    category = flask.request.args.get('category')
    if category == 'selectCategory' or category is None:
        category = ''
    category = '%' + category + '%'
    
    order = flask.request.args.get('order')
    if order == 'order' or order is None:
        order = ''
    order = '%' + order + '%'
        
    family = flask.request.args.get('family')
    if family == 'family' or family is None:
        family = ''
    family = '%' + family + '%'
        
    park_code = flask.request.args.get('park_code')
    if park_code == 'selectPark' or park_code is None :
        park_code = ''
    park_code = '%' + park_code + '%'
        
    state = flask.request.args.get('state')
    if state == 'selectState' or state is None:
        state = ''
    state = '%' + state + '%'
    print(species_name, species_name, category, order, family, park_code, state)
    query = '''SELECT species.common_names, species.scientific_name, categories.category, orders.order_name,
                families.family, species.nativeness, parks.park_code, states.id                    
                FROM species, categories, orders, families, states, parks
                WHERE (species.common_names iLIKE %s OR species.scientific_name iLIKE %s)
                AND species.category_id = categories.id
                AND species.order_id = orders.id
                AND orders.order_name iLIKE %s
                AND categories.category iLIKE %s
                AND species.family_id = families.id
                AND families.family iLIKE %s
                AND species.park_code iLIKE %s
                AND parks.state_code iLIKE %s
                AND parks.state_code iLIKE concat('%%', states.id, '%%')
                AND species.park_code = parks.park_code
                ORDER BY species.scientific_name'''
#    SELECT species.common_names, species.scientific_name, categories.category, orders.order, 
#                    families.family, species.nativeness, parks.park_name, states.id
#                    FROM species, categories, orders, families, states, parks 
#                    WHERE species.common_names LIKE %s
#                    OR species.scientific_name LIKE %s
#                    AND categories.category LIKE %s
#                    AND orders.order LIKE %s
#                    AND families.family LIKE %s
#                    AND parks.park_name LIKE %s
#                    AND parks.state_code LIKE %s
#                    AND species.park_code = park.park_code
#                    AND parks.state_code = states.id
#                    AND species.category_id = category.id
#                    AND species.order_id = orders.id
#                    AND species.family_id = family.id
#                    ORDER BY species.scientific_name
#     AND parks.state_code LIKE CONCAT('%', states.id, '%')
    
    species_results = []
    parks = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (species_name, species_name, order, category, family, park_code, state))
        print(cursor.query)

        results = {}
        for row in cursor:
            if row[1] in results:
                temp = results[row[1]]
                if row[7] not in temp['state']:
                        temp['state'].append(row[7])
                        
                if row[5] == 'Native' and (' ' + row[6]) not in temp['nativeTo']:
                    temp['nativeTo'].append(' ' + row[6])

                elif row[5] == 'Not Native' and (' ' + row[6]) not in temp['notNative']:
                    temp['notNative'].append(' ' + row[6])
                    
                elif row[5] == 'Unknown' or row[5] == 'Present' or row[5] == 'Not Confirmed':
                    if (' ' + row[6]) not in temp['unknown']:
                        temp['unknown'].append(' ' + row[6])

            else:
                if row[5] == 'Native':
                    results[row[1]] = {'common_name': row[0], 'scientific_name': row[1], 'category': row[2],
                    'order': row[3], 'family': row[4], 'nativeTo': [' ' + row[6]], 'notNative': [], 'unknown':[], 'state':[row[7]]}

                elif row[5] == 'Not Native':
                    results[row[1]] = {'common_name': row[0], 'scientific_name': row[1], 'category': row[2],
                                       'order': row[3], 'family': row[4], 'nativeTo': [], 'notNative': [' ' + row[6]],
                                       'unknown': [], 'state': [row[7]]}
                else:
                    results[row[1]] = {'common_name': row[0], 'scientific_name': row[1], 'category': row[2],
                                       'order': row[3], 'family': row[4], 'nativeTo': [], 'notNative': [],
                                       'unknown': [' ' + row[6]], 'state': [row[7]]}

            # species = {'common_name': row[0], 'scientific_name': row[1], 'category': row[2],
            #         'order': row[3], 'family': row[4], 'nativeness': row[5], 'park_name':row[6], 'state':[row[7]]}
            # species_results.append(species)
        print(len(results))
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

        # Filtering out the redundant results


    
    return json.dumps(results)


@api.route('/species_search/categories', strict_slashes=False)
def load_categories():
    return json.dumps(get_category())


@api.route('/species_search/states', strict_slashes=False)
def load_states_species():
    return json.dumps(get_state())


@api.route('/species_search/parks', strict_slashes=False)
def load_parks_species():
    return json.dumps(get_park_info())


@api.route('/help/')
def help():
    help_text = open('templates/help.txt').read()
    return flask.Response(help_text, mimetype='text/plain')








