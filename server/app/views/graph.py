import os
import json
from flask import request, Blueprint, jsonify
from thefuzz import process


mod = Blueprint('graph', __name__, url_prefix='/graph')


@mod.route('/', methods=['GET'])
def graph():
    with open('data/data.json', 'r') as f:
        data = json.load(f)

    return jsonify({
        'data': data,
        'message': 'You Got It!'
    })


# @mod.route('/search', methods=['GET'])
# def get_triples():
#     # 获取参数
#     user_input = request.args.get('search')
#     result = search_node_item(user_input)

#     return jsonify({
#         'data': result,
#         'message': 'Got it!'
#     })
