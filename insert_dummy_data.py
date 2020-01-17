import pymongo
import os # for environment variables

mongo_url =  "mongodb://" + os.environ['MONGODB_NAME'] + ":" + \
    os.environ['MONGODB_PASS'] + "@" + \
    os.environ['MONGODB_LINK'] + "?ssl=true&replicaSet=HorusMongoDB-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_url)

db = client.horus

users = [
  {
    "name": "hans wurst",
    "dob": "27.04.1997",
    "group": "marketing"
  },
  {
    "name": "gerald wimmer",
    "dob": "31.08.1993",
    "group": "hr"
  },
  {
    "name": "anna fakename",
    "dob": "14.12.1987",
    "group": "management"
  },
  {
    "name": "harry potter",
    "dob": "24.05.1965",
    "group": "defense"
  },
  {
    "name": "franz bauer",
    "dob": "01.01.2000",
    "group": "maintenance"
  }
]

ids = db.user.insert_many(users).inserted_ids


sicknesses = [
  {
    "user": ids[0],
    "sickdays": [
      "10.12.2019",
      "11.12.2019"
    ]
  },
  {
    "user": ids[4],
    "sickdays": [
      "06.01.2020",
      "07.01.2020",
      "08.01.2020",
      "09.01.2020",
      "10.01.2020",
    ]
  },
]

db.sickness.insert_many(sicknesses)