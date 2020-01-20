import pymongo
import os # for environment variables
from datetime import datetime

mongo_url =  "mongodb://" + os.environ['MONGODB_NAME'] + ":" + \
    os.environ['MONGODB_PASS'] + "@" + \
    os.environ['MONGODB_LINK'] + "?ssl=true&replicaSet=HorusMongoDB-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_url)

db = client.horus

def findByName(name):
   return db.user.find({"name": name})

def findSicknessByUserId(id):
    return db.sickness.find({"user": id})

def addSicknessToUser(name, date):
    entry = findByName(name)

    if entry is None or entry.count() == 0:
        return None

    user = entry.next()

    db.sickness.update_one(
        { 'user': user['_id']},
        { '$addToSet': {
                'sickdays': date
            }
        },
        True) #upsert

    return user

date_time_format = '%Y-%m-%dT%H:%M:%S%z'

def addVacation(user_name, start, end):
    entry = findByName(user_name)

    if entry is None or entry.count() == 0:
        return False

    user = entry.next()

    db.vacation.insert_one({
        'user': user['_id'],
        'start': datetime.strptime(start, date_time_format),
        'end': datetime.strptime(end, date_time_format)
    })

    return True
    # 2012-12-12T12:00:00+01:00"

def getAllSickUsers():
    sicknesses = db.sickness.aggregate([
        {
            '$lookup': {
                'from': 'user',
                'localField': 'user',
                'foreignField': '_id',
                'as': 'userobj'
            }
        }, {
            '$project': {
                'user': {
                    '$arrayElemAt': [
                        '$userobj', 0
                    ]
                },
                'sickdays': 1
            }
        }
    ])
    result = {}

    for sick_user in sicknesses:
        result[sick_user['user']['name']] = sick_user['sickdays']

    return result

def getAllVacations():
    return db.vacation.aggregate([
        {
            '$lookup': {
                'from': 'user',
                'localField': 'user',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$project': {
                'user': {
                    '$arrayElemAt': [
                        '$user', 0
                    ]
                },
                'start': 1,
                'end': 1
            }
        }
    ])
