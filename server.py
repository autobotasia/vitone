import flask 
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import os
import io
import re
import sys
import json
from tensor2tensor import problems as problems_lib
from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import hparam
from tensor2tensor.utils import registry
import problems


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

def make_request_fn():
    """Returns a request function."""
    request_fn = serving_utils.make_grpc_request_fn(
        servable_name="vitone",
        server="localhost:9000",
        timeout_secs=10)
    return request_fn


problem = registry.problem("translate_vivi")
hparams = hparam.HParams(data_dir=os.path.expanduser("./data/translate_vivi"))
problem.get_hparams(hparams)
request_fn = make_request_fn()

@app.route('/check', methods=['POST']) 
def face():
    replacements = []
    rules = []
    data = request.json
    confident = 0
    for txt in data["text"]:
        text = txt["text"]
        offset = txt["offset"]
        outputs = serving_utils.predict([text], problem, request_fn)
        outputs, = outputs
        output, confident = outputs
        rule = AuRule("MORFOLOGIK_RULE_EN_US", "Possible spelling mistake", "misspelling", None)
        replacement = AuReplacement(text, output, offset, len(text), None)        
        rules.append(rule)
        replacements.append(replacement)
        #matches.append(match)

    matches = AuMatch("Tự động thêm dấu", "Tự động thêm dấu", replacements, rules)
    ret = AuResult(AuLanguage("Vietnamese (Vi)", "vi-VN"), AuLanguage("Vietnamese (Vi)", "vi-VN"), matches, confident)    
    return ret.toJSON()


