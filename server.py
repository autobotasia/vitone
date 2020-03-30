import flask 
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import io
import re
import sys
import json


app = Flask(__name__)
CORS(app, support_credentials=True)

class JsonSerialize:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class AuLanguage(JsonSerialize):
    def __init__(self, name, code):
        self.name = name
        self.code = code

class AuMatch(JsonSerialize):
    def __init__(self, message, shortMessage, replacements, rules):
        self.message = message
        self.shortMessage = shortMessage
        self.replacements = replacements
        self.rules = rules

class AuReplacement(JsonSerialize):
    def __init__(self, origin, replaceby, offset, length, type):
        self.origin = origin
        self.replaceby = replaceby
        self.offset = offset
        self.length = length
        self.type = type

class AuRule(JsonSerialize):
    def __init__(self, id, description, issue_type, category):
        self.id = id
        self.description = description
        self.issue_type = issue_type
        self.category = category

class AuResult(JsonSerialize):
    def __init__(self, orgLang, detectLang, matches, confident):
        self.orgLang = orgLang
        self.detectLang = detectLang
        self.matches = matches
        self.confidence = confident


@app.route('/check', methods=['POST']) 
def face():
    replacements = []
    rules = []
    data = request.json
    for txt in data["text"]:
        text = txt["text"]
        offset = txt["offset"]
        rule = AuRule("MORFOLOGIK_RULE_EN_US", "Possible spelling mistake", "misspelling", None)
        replacement = AuReplacement(text, text, offset, len(text), None)        
        rules.append(rule)
        replacements.append(replacement)
        #matches.append(match)

    matches = AuMatch("Tự động thêm dấu", "Tự động thêm dấu", replacements, rules)
    ret = AuResult(AuLanguage("Vietnamese (Vi)", "vi-VN"), AuLanguage("Vietnamese (Vi)", "vi-VN"), matches, 0.9)    
    return ret.toJSON()


