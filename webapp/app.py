#!/usr/bin/env python3
'''
    Jeff Ondich
    Updated: 5 November 2021

    A tiny Flask web application, including API and Javascript,
    to be used as a template for setting up your web app assignment.
'''
import argparse
import flask
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/about/')
def about():
    return flask.render_template('about_page.html')


@app.route('/park_search/')
def park_search():
    return flask.render_template('park_search.html')


@app.route('/species_search/')
def species_search():
    return flask.render_template('species_search.html')

@app.route('/help/')
def help():

    return flask.render_template('help.txt')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tiny Flask application, including API')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
