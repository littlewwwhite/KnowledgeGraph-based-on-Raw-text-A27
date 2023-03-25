import os
import json
from flask import request, Blueprint, jsonify


mod = Blueprint('graph', __name__, url_prefix='/graph')


@mod.route('/', methods=['GET'])
def graph():
    with open('data/data.json', 'r') as f:
        data = json.load(f)

    return jsonify({
        "data": data,
        "message": "You Got It!"
    })
