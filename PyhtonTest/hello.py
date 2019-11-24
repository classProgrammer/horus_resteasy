from flask import Flask, request, make_response, jsonify, abort
import sys
from datetime import date


myapp = Flask(__name__)

users = {
    "hans wurst27.04.1997": True
}

sickness = {}

@myapp.route("/")
def hello():
    return "The REST service is up"

@myapp.route("/authenticate", methods=['POST'])
def authenticate():

    data = request.get_json()
    key = data['name'].lower() + data['dob']
    
    if not(key in users):
        return "ERROR: invalid parameters", 400

    return "", 200
    
@myapp.route("/add/user", methods=['POST'])
def adduser():
  
    data = request.get_json()
    key = data['name'].lower() + data['dob']
    
    if not(key in users):
        users[key] = True

    return "Resource created", 202

@myapp.route("/sick", methods=['POST'])
def addsick():
    data = request.get_json()
    key = data['name'].lower() + data['dob']
    today = date.today()
    date_ = today.strftime("%d.%m.%Y")
    
    if not(key in users):
        return "ERROR: invalid parameters", 400

    if not(key in sickness):
        sickness[key] = []

    if not(date_ in sickness[key]):
        sickness[key].append(date_)

    return date_, 202

@myapp.route("/sick", methods=['GET'])
def getsick():
    data = request.get_json()
    key = data['name'].lower() + data['dob']
    
    if not(key in sickness):
        return "ERROR: invalid parameters", 400
    if len(sickness[key]) < 1:
        return "No entry found", 200
    

    return sickness[key][-1], 202

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    
    #print("req", req)

    # fetch action from json
    #action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}

# create a route for webhook
@myapp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))