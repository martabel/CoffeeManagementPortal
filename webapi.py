from flask import Blueprint, request,Response, redirect, url_for
from functools import wraps
import database

from bson.json_util import dumps as bsonDumps
from json import loads as jsonLoads
from flask import jsonify

webapi = Blueprint('webapi', __name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'wurst'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@webapi.route('/coffeelist', methods = ['GET'])
@webapi.route('/coffeelist/<id>', methods = ['GET'])
def getCoffeeList(id=None):
    cList = None
    if id==None:
        cList = database.getLastCoffeeList()
    else:
        cList = database.getCoffeeListbyId(id=id)

    resp = Response(
        response=bsonDumps(cList),
        status=200,
        mimetype="application/json")

    return resp

@webapi.route('/drinkerlist', methods = ['GET'])
@webapi.route('/drinkerlist/<id>', methods = ['GET'])
def getDrinkerList(id=None):
    dList = None
    if id==None:
        dList = database.getLastDrinkerList()
    else:
        dList = database.getDrinkerListbyId(id=id)

    resp = Response(
        response=bsonDumps(dList),
        status=200,
        mimetype="application/json")

    return resp

@webapi.route('/syncCoffees', methods=['POST'])
@requires_auth
def sync_coffees():
    print request.data
    database.saveCoffees(request.data)
    return "OK"

@webapi.route('/syncDrinkers', methods=['POST'])
@requires_auth
def sync_drinkers():
    print request.data
    database.saveDrinkers(request.data)
    return "OK"
