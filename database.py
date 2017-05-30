import pymongo, datetime, json
from StringIO import StringIO
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps as bsonDumps

client = MongoClient('mongodb://localhost:27017/')
db = client['coffee']

def getDrinkerLists():
    drinkerLists = []
    #filter only id and timestamp
    for dList in db.drinkerLists.find():
        drinkerLists.append({'_id':dList['_id'], 'timestamp':dList['timestamp']})
    return drinkerLists

def getCoffeeLists():
    coffeeLists = []
    #filter only id and timestamp
    for cList in db.coffeeLists.find():
        coffeeLists.append({'_id':cList['_id'], 'timestamp':cList['timestamp']})
    return coffeeLists

def getLastDrinkerList():
    return db.drinkerLists.find_one()

def getDrinkerListbyId(id):
    return db.drinkerLists.find_one({'_id': ObjectId(id)})

def getLastCoffeeList():
    cLists = []
    for cList in db.coffeeLists.find().sort("timestamp", -1).limit(1)[0]['Coffees']:
        for drinker in db.drinkerLists.find().sort("timestamp", -1).limit(1)[0]['CoffeeDrinker']:
            print cList['CoffeeCosumer_Id']
            print drinker['ID']
            if int(drinker['ID']) == int(cList['CoffeeCosumer_Id']):
                cList['CoffeeCosumer_Id'] = drinker
                break
        cLists.append(cList)
    return cLists

def getCoffeeListbyId(id):
    return db.coffeeLists.find_one({'_id': ObjectId(id)})

def saveCoffees(coffeesJSON):
    #load json string
    coffeeListEntry = json.load(StringIO(coffeesJSON))
    #add  timestamp
    coffeeListEntry['timestamp'] = datetime.datetime.utcnow()
    #save in db
    db.coffeeLists.insert_one(coffeeListEntry)

def saveDrinkers(drinkersJSON):
    #load json string
    drinkerListEntry = json.load(StringIO(drinkersJSON))
    #add  timestamp
    drinkerListEntry['timestamp'] = datetime.datetime.utcnow()
    #save in db
    db.drinkerLists.insert_one(drinkerListEntry)
