#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, url_for
from flask.ext.pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
mongo = PyMongo(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/safetytips/api/v1.0/tips/', methods=['GET'])
def get_tips():
    tips = mongo.db.tips.find()
    return jsonify({'tips': tips})

@app.route('/safetytips/api/v1.0/tips/<int:tip_id>', methods=['GET'])
def get_tip(incoming_tip_id):
    tip = mongo.db.tips.find({'tip_id': incoming_tip_id})[0]
    if not tip:
        abort(404)
    return jsonify({'tip': tip})

@app.route('/safetytips/api/v1.0/tips/', methods=['POST'])
def create_tip():
    if not request.json or not 'title' in request.json:
        abort(400)

    tip = {
        'tip_id': mongo.db.tips.find()[-1]['tip_id'] + 1,
        'created_at': datetime.datetime.now(),
        'last_updated': datetime.datetime.now(),
        'message': request.json['message'],
        'original_message': request.json['message'],
        'username': request.json['username'],
    }

    mongo.db.tips.save(tip)
    return jsonify({'tip': tip}), 201

@app.route('/safetytips/api/v1.0/tips/<int:tip_id>', methods=['POST'])
def update_tip(incoming_tip_id):
    if not tip or not request.json or not request.json['username'] or not request.json['message']:
        abort(404)
    mongo.db.tips.update(
        {'tip_id': incoming_tip_id},
        {
            $set: {
                last_updated: datetime.datetime.now(),
                message: request.json['message'],
                username: request.json['username']
            }
        },
    )
    tip = mongo.db.tips.find({'tip_id': tip_id})[0]
    return jsonify({'tip': tip}), 201


@app.route('/safetytips/api/v1.0/tips/<int:tip_id>', methods=['DELETE'])
def delete_tip(incoming_tip_id):
    tip = mongo.db.tips.find({'tip_id': incoming_tip_id})[0]
    mongo.db.tips.remove({'tip_id': incoming_tip_id}, 1)
    return jsonify({'result': True})