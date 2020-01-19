from flask import Flask, request, make_response, jsonify, abort
import sys
from datetime import date
import re
import pymongo
import os # for environment variables
from bson import json_util

mongo_url =  "mongodb://" + os.environ['MONGODB_NAME'] + ":" + \
    os.environ['MONGODB_PASS'] + "@" + \
    os.environ['MONGODB_LINK'] + "?ssl=true&replicaSet=HorusMongoDB-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_url)

db = client.horus

restService = Flask(__name__)

# ----------------------------------------------
# -------------------- DATA --------------------
# ----------------------------------------------
dialogflow_request = [""]
watson_request = [""]

# ----------------------------------------------
# --------------- UTILITY METHODS --------------
# ----------------------------------------------
def findByName(name):
  return db.user.find({"name": name})

def now():
    return date.today().strftime("%d.%m.%Y")

def asJsonResponse(data):
    return make_response(jsonify(data))

def extractDob(date):
    pattern = re.compile(r"[-T+]")
    return '.'.join(reversed(pattern.split(date)[0:3]))

# ----------------------------------------------
# ----------------- STARTUP --------------------
# ----------------------------------------------
@restService.route("/")
def default():
    return "The REST service is up"

# ----------------------------------------------
# ------------------- RASA ---------------------
# ----------------------------------------------
# entry point for Rasa call
@restService.route("/sick", methods=['POST'])
def postSick():
    data  = request.get_json()
    name  = data['name'].lower()

    entry = findByName(name)

    if (len(entry) < 1):
        return "ERROR: invalid parameters", 400

    today = now()

    if not(name in sickness):
        sickness[name] = []

    if not(today in sickness[name]):
        sickness[name].append(today)

    return {
        "name": data['name'],
        "group": entry[0]["group"],
        "dob": entry[0]["dob"],
        "sick_on": today
    }, 200

# ----------------------------------------------
# ---------------- DIALOGFLOW ------------------
# ----------------------------------------------
def dialogflowHandler():
    req = request.get_json(force=True)
    dialogflow_request[0] = req #DEV
    intent = req.get('queryResult').get('intent').get("displayName")

    if (intent == "Sickness"):
        params = req.get('queryResult').get('parameters')
        name = params.get("name").get("name").lower()
        today = now()
        if (len(findByName(name)) < 1):
            return {'fulfillmentText': 'Die eingegebenen Daten sind ungültig. Die Konversation wird zurückgesetzt'}
        
        if not(name in sickness):
            sickness[name] = []

        if not(today in sickness[name]):
            sickness[name].append(today)
        
        return {}

    return {'fulfillmentText': f'Intent {intent} unbekannt.'}

# dialogflow request entry point
@restService.route('/dialogflow/webhook', methods=['GET', 'POST'])
def dialogflowWebhook():
    return asJsonResponse(dialogflowHandler())

# ----------------------------------------------
# ------------------ WATSON --------------------
# ----------------------------------------------  
def watsonHandler():
    req = request.get_json(force=True)
    intent = req.get('intent')
    watson_request[0] = req #DEV
    if (intent == "Sickness"):

        name = req.get("person_name").lower()
        today = now()
        
        if (len(findByName(name)) < 1):
            return {'error': 'Die eingegebenen Daten sind ungültig.'}
        
        if not(name in sickness):
            sickness[name] = []

        if not(today in sickness[name]):
            sickness[name].append(today)
        
        return {'OK': f'Gute Besserung {req.get("person_name")}!'}

    return {'error': f'Intent {intent} unbekannt.'}

# watson request entry point
@restService.route('/watson/webhook', methods=['POST'])
def watsonWebhook():
    return asJsonResponse(watsonHandler())

# ----------------------------------------------
# -------------- DEVELOPMENT -------------------
# ----------------------------------------------
@restService.route("/sick/all", methods=['GET'])
def getSickAll():
    return asJsonResponse(sickness), 200

# For dev purpose/check
@restService.route("/sick", methods=['GET'])
def getSick():
    data = request.get_json()
    name = data['name']

    user = findByName(name)

    if user is None or user.count() == 0:
        return "ERROR: invalid parameters", 400

    sicknesses = db.sickness.find({"user": user.next()['_id']})

    if sicknesses.count() == 0:
        return "No entry found", 200
    else:
        return json_util.dumps(sicknesses)

# for dev purpose, to check what the framewokrs send
@restService.route("/dialogflow/requests", methods=['GET'])
def getRequests():
    return asJsonResponse(dialogflow_request), 200

@restService.route("/watson/requests", methods=['GET'])
def getWatsonRequests():
    return asJsonResponse(watson_request), 200