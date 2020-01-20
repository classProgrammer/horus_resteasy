import pymongo
import os # for environment variables

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