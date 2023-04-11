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


@mod.route('/search', methods=['GET'])
def get_triples():
    # 获取参数
    user_input = request.args.get('search')
    result = search_node_item(user_input)

    return jsonify({
        'data': result,
        'message': 'Got it!'
    })

def search_node_item(user_input, lite_graph=None):
    with open('data/data.json', 'r') as f:
        data = json.load(f)

    if lite_graph is None:
        lite_graph = {
            'nodes': [],
            'links': [],
            'sents': []
        }

    # 利用thefuzz库来选取最相近的节点
    # node_names = [node['name'] for node in data['nodes']]
    # user_input = process.extractOne(user_input, node_names)[0]

    DEEP = 1

    # search node
    search_nodes = [user_input]
    for d in range(DEEP):
        for serch_node in search_nodes:
            for edge in data['links']:
                source = data['nodes'][int(edge['source'])]
                target = data['nodes'][int(edge['target'])]
                if source['name'] in serch_node or serch_node in source['name'] or target['name'] in serch_node or serch_node in target['name']:
                # if source['name'] == serch_node or target['name'] == serch_node:
                    sent = data['sents'][edge['sent']]
                    if sent not in lite_graph['sents']:
                        edge['sent'] = len(lite_graph['sents'])
                        lite_graph['sents'].append(sent)
                    else:
                        edge['sent'] = lite_graph['sents'].index(sent)

                    if source not in lite_graph['nodes']:
                        source['id'] = len(lite_graph['nodes'])
                        lite_graph['nodes'].append(source)
                    else:
                        source['id'] = lite_graph['nodes'].index(source)

                    if target not in lite_graph['nodes']:
                        target['id'] = len(lite_graph['nodes'])
                        lite_graph['nodes'].append(target)
                    else:
                        target['id'] = lite_graph['nodes'].index(target)

                    edge['source'] = source['id']
                    edge['target'] = target['id']
                    lite_graph['links'].append(edge)

        if len(lite_graph['nodes']) == 0:
            break

        search_nodes = [node['name'] for node in lite_graph['nodes']]

    return lite_graph