import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    # gets drinks from the database to the public
    drink = Drink.query.all()
    drinks = [drinkss.short() for drinkss in drink]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(self):
    # query database for drinks
    drink = Drink.query.all()
    drinks = [drinkss.long() for drinkss in drink]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(self):
    # gets data from the client
    body = request.get_json()
    if not body:
        abort(404)
    req_title = body.get('title')
    req_recipe = json.dumps(body.get('recipe'))
    # adds a drink to database
    add_drink = Drink(title=req_title, recipe=req_recipe)
    add_drink.insert()
    drink = add_drink.long()

    return jsonify({
        'success': True,
        'drinks': drink
    })


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True,
    "drinks": drink} where drink an array containing only
    the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(self, id):
    # gets data from client
    body = request.get_json()
    if not body:
        abort(404)
    # gets drink to be updated
    get_drink = Drink.query.filter(Drink.id == id).one_or_none()
    if get_drink is None:
        abort(404)
    # updates the drink on the server
    get_drink.title = body.get('title')
    get_drink.update()
    drink = get_drink.long()
    return jsonify({
        'success': True,
        'drinks': drink
    })


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def trash_drinks(self, id):
    # gets drink to delete
    trash_drink = Drink.query.get(id)
    if trash_drink is None:
        abort(404)
    # deletes drink
    trash_drink.delete()
    return jsonify({
        'success': True,
        'delete': trash_drink.id
    })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal_server_error'
    }), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method_not_allowed'
    }), 405


'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def AuthError(error):
    response = jsonify(error)
    response.status_code = error.status_code

    return response
