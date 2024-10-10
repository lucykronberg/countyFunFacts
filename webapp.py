from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    states = get_state_options()
    #print(states)
    return render_template('home.html', state_options=states)

@app.route('/showFact')
def render_fact():
    states = get_state_options()
    state = request.args.get('state')
    counties = get_county_options(state)
    county = county_most_under_18(state)
    fact = "In " + state + ", the county with the highest percentage of under 18 year olds is " + county + "."
    county1 = education (state)
    fact1 = "In " + state + ", the county with the highest percentage of education of high school or higher is " + county1 + "."
    return render_template('home.html', state_options=states, county_options=counties, funFact=fact, anotherFunFact=fact1)
    
@app.route('/showFact1')
def render_fact1():
    states = get_state_options()
    county = request.args.get('county')
    countyP = population(county)
    fact1 = "In " + county + ", population per square mile is " + str(countyP) + "."
    return render_template('home.html', state_options=states, county_options=countyP, anotherFunFact=fact1)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_county_options(state):
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    states=[]
    for c in counties:
        if c["State"] == state:
            if c["County"] not in states:
                states.append(c["County"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county

def education(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county1 = ""
    for c in counties:
        if c["State"] == state:
            if c["Education"]["High School or Higher"] > highest:
                highest = c["Education"]["High School or Higher"]
                county1 = c["County"]
    return county1
    
def population(county):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    countyP = ""
    for c in counties:
        if c["County"] == county:
            return c["Population"]["Population per Square Mile"]
    return countyP
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
