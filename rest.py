from flask import Flask, request, make_response, jsonify, abort
import sys
from datetime import date
import re

restService = Flask(__name__)

# ----------------------------------------------
# -------------------- DATA --------------------
# ----------------------------------------------
dialogflow_request = [""]
watson_request = [""]

# ----------------------------------------------
# --------------- UTILITY METHODS --------------
# ----------------------------------------------
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
# ---------------- DIALOGFLOW ------------------
# ----------------------------------------------
def personNotFound(str):
    return "Person not found. Enter " + str + " to retry."

def dialogflowRequestHandler():
    req = request.get_json(force=True)
    dialogflow_request[0] = req #DEV
    intent = req.get('queryResult').get('intent').get('displayName')

    if (intent == 'Sickness'):
        params = req.get('queryResult').get('outputContexts')[0].get('parameters')
        employee_name = params.get('employee').get('name').lower()
    elif (intent == 'Sickness Confirmed'):
        params = req.get('queryResult').get('outputContexts')[0].get('parameters')
        employee_name = params.get('employee').get('name').lower()
        # today = now()

        return {
            "fulfillmentMessages": [
                {
                "text": {
                    "text": [
                    "Text response from webhook"
                    ]
                }
                }
            ]
        }
        
    elif (intent == 'Vacation'):
        # params = req.get('queryResult').get('parameters')
        # name = params.get('name').get('name').lower()
        # start = params.get('start')
        # end = params.get('end')

        return {'fulfillmentText': 'vacation intent'}

    return {
            "fulfillmentMessages": [
                {
                "text": {
                    "text": [
                    f'Intent {intent} unknown.'
                    ]
                }
                }
            ]
        }

def watsonRequestHandler():
    req = request.get_json(force=True)
    intent = req.get('intent')
    watson_request[0] = req #DEV
    if (intent == "Sick"):

        name = req.get("person_name").lower()
        today = now()

    return {
        'OK': True,
        'Department': 'Marketing'
        }

# dialogflow request entry point
@restService.route('/dialogflow/webhook', methods=['GET', 'POST'])
def dialogflowRequestEntryPoint():
    return asJsonResponse(dialogflowRequestHandler()), 200

@restService.route('/watson/webhook', methods=['GET', 'POST'])
def watsonRequestEntryPoint():
    return asJsonResponse(watsonRequestHandler()), 200


# ----------------------------------------------
# -------------- DEVELOPMENT -------------------
# ----------------------------------------------
@restService.route("/sick/all", methods=['GET'])
def getSickAll():
    return {}, 200

# For dev purpose/check
@restService.route("/sick", methods=['GET'])
def getSick():
    return {}, 200

# for dev purpose, to check what the framewokrs send
@restService.route("/dialogflow/requests", methods=['GET'])
def getRequests():
    return asJsonResponse(dialogflow_request), 200

@restService.route("/watson/requests", methods=['GET'])
def getWatsonRequests():
    return asJsonResponse(watson_request), 200

date_time_format = '%Y-%m-%dT%H:%M:%S%z'

@restService.route("/vacation/all", methods=['GET'])
def getVacationAll():
    return {}, 200
