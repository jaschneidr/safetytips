#!flask/bin/python


import datetime
import json

from flask import Flask, abort, make_response, request
from flask.ext.pymongo import PyMongo
from werkzeug import Response

from bson.objectid import ObjectId


app = Flask(__name__)
mongo = PyMongo(app)


class MongoDBJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoDBJsonEncoder), mimetype='application/json')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 400)

@app.route('/safetytips/api/v1.0/tips/', methods=['GET'])
def get_tips():
    tips = mongo.db.tips.find()
    if tips:
        return jsonify({'tips': [tip for tip in tips]}), 200
    else:
        abort(400)

@app.route('/safetytips/api/v1.0/tips/<int:incoming_tip_id>', methods=['GET'])
def get_tip(incoming_tip_id):
    tip = mongo.db.tips.find({'tip_id': incoming_tip_id})[0]
    if not tip:
        abort(404)
    return jsonify({'tip': tip}), 200

@app.route('/safetytips/api/v1.0/tips/', methods=['POST'])
def create_tip():
    if not request.json or not 'username' in request.json:
        abort(400)

    tip = {
        'tip_id': len([tip for tip in mongo.db.tips.find()]) + 1,
        'created_at': datetime.datetime.now(),
        'last_updated': datetime.datetime.now(),
        'message': request.json['message'],
        'original_message': request.json['message'],
        'username': request.json['username'],
    }

    mongo.db.tips.save(tip)
    created_tip = [tip for tip in mongo.db.tips.find()][-1]
    return jsonify({'tip': created_tip}), 201

@app.route('/safetytips/api/v1.0/tips/<int:incoming_tip_id>', methods=['PUT'])
def update_tip(incoming_tip_id):
    tip = mongo.db.tips.find({'tip_id': incoming_tip_id})[0]

    if not tip or not request.json:
        abort(404)

    mongo.db.tips.update(
        {'tip_id': incoming_tip_id},
        {"$set": {
            'last_updated': datetime.datetime.now(),
            'message': request.json['message'],
            'username': request.json['username']
        }},
        upsert=True
    )
    updated_tip = mongo.db.tips.find({'tip_id': incoming_tip_id})[0]
    return jsonify({'tip': updated_tip}), 201

@app.route('/safetytips/api/v1.0/tips/<int:incoming_tip_id>', methods=['DELETE'])
def delete_tip(incoming_tip_id):
    tip = mongo.db.tips.find({'tip_id': incoming_tip_id})[0]
    mongo.db.tips.remove({'tip_id': incoming_tip_id})
    return jsonify({'result': True}), 202

if __name__ == '__main__':
    app.run()

