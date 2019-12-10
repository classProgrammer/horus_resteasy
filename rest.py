from flask import Flask, request, make_response, jsonify, abort
import sys
from datetime import date
import re

restService = Flask(__name__)

users = {
    "hans wurst27.04.1997": True,
    "gerald wimmer31.08.1993": True,
    "anna fakename14.12.1987": True,
    "harry potter24.05.1965": True,
    "franz bauer01.01.2000": True
}

sickness = {}

requests = []
watson_requests = []

@restService.route("/")
def default():
    return "The REST service is up"

@restService.route("/authenticate", methods=['POST'])
def authenticate():

    data = request.get_json()
    key = data['name'].lower() + data['dob']
    
    if not(key in users):
        return "ERROR: invalid parameters", 400

    return "", 200
    
@restService.route("/add/user", methods=['POST'])
def addUser():
  
    data = request.get_json()
    key = data['name'].lower() + data['dob']
    
    if not(key in users):
        users[key] = True

    return "Resource created", 202

@restService.route("/sick", methods=['POST'])
def postSick():
    data = request.get_json()
    key = data['name'].lower() + data['dob']
    today = date.today()
    formatted_date = today.strftime("%d.%m.%Y")
    
    if not(key in users):
        return "ERROR: invalid parameters", 400

    if not(key in sickness):
        sickness[key] = []

    if not(formatted_date in sickness[key]):
        sickness[key].append(formatted_date)

    return formatted_date, 200

@restService.route("/sick", methods=['GET'])
def getSick():
    data = request.get_json()
    key = data['name'].lower() + data['dob']
    
    if not(key in sickness):
        return "ERROR: invalid parameters", 400
    if len(sickness[key]) < 1:
        return "No entry found", 200

    return sickness[key][-1], 200

@restService.route("/dialogflow/requests", methods=['GET'])
def getRequests():
    return asJsonResponse(requests)

@restService.route("/watson/requests", methods=['GET'])
def getWatsonRequests():
    return asJsonResponse(watson_requests)

@restService.route("/sick/all", methods=['GET'])
def getSickAll():
    return asJsonResponse(sickness)

def extractDob(date):
    pattern = re.compile(r"[-T+]")
    return '.'.join(reversed(pattern.split(date)[0:3]))

def dialogflowHandler():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    intent = req.get('queryResult').get('intent').get("displayName")

    if (intent == "Sickness"):
        params = req.get('queryResult').get('parameters')
        name = params.get("name").get("name")
        dob = extractDob(params.get("dob"))

        requests.append(req)
        key = name.lower() + dob
        today = date.today()
        formatted_date = today.strftime("%d.%m.%Y")
        
        if not(key in users):
            return {'fulfillmentText': 'Die eingegebenen Daten sind ungültig. Die Konversation wird zurückgesetzt'}
        
        if not(key in sickness):
            sickness[key] = []

        if not(formatted_date in sickness[key]):
            sickness[key].append(formatted_date)
        
        return {}


def asJsonResponse(data):
    return make_response(jsonify(data))

# create a route for webhook
@restService.route('/dialogflow/webhook', methods=['GET', 'POST'])
def dialogflowWebhook():
    # return response
    return asJsonResponse(dialogflowHandler())


def watsonHandler():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    intent = req.get('intent')

    if (intent == "Sickness"):

        name = req.get("person_name")
        dob = extractDob(req.get("dob"))

        watson_requests.append(req)
        key = name.lower() + dob
        today = date.today()
        formatted_date = today.strftime("%d.%m.%Y")
        
        if not(key in users):
            return {'error': 'Die eingegebenen Daten sind ungültig.'}
        
        if not(key in sickness):
            sickness[key] = []

        if not(formatted_date in sickness[key]):
            sickness[key].append(formatted_date)
        
        return {'OK': 'Gute Besserung'}

# create a route for webhook
@restService.route('/watson/webhook', methods=['POST'])
def watsonWebhook():
    return asJsonResponse(watsonHandler())