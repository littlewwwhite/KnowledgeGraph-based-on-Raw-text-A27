# coding=utf-8
from flask import Flask, jsonify
from flask_cors import CORS
from app.utils.chat_glm import start_model

apps = Flask(__name__)# 这段代码是为了解决跨域问题，Flask默认不支持跨域
CORS(apps, resources=r'/*')# CORS的用法是

from app.views import chat, graph
apps.register_blueprint(chat.mod)
apps.register_blueprint(graph.mod)


@apps.route('/', methods=["GET"])
def route_index():
    return jsonify({"message": "You Got It!"})


@apps.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "DEBUG: " + str(e)}), 404


@apps.errorhandler(403)
def page_not_found(e):
    return jsonify({"message": str(e)}), 403

