#!/usr/bin/env python
# coding: utf-8
import os
import sys
import json
from flask import Flask, jsonify, request


app = Flask(__name__)
app.config['DEBUG'] = True

SOURCE_FILE='test.jsonl'
RESULT_FILE='result.jsonl'

exs  = [json.loads(l) for l in open(SOURCE_FILE)]
saved = {}

# Recover
if os.path.exists(RESULT_FILE):
    for line in open(RESULT_FILE):
        data = json.loads(line)
        saved[data['query_id']] = data['option']

for i, ex in enumerate(exs):
    if ex['query_id'] in saved:
        continue
    else:
        break

idx = i - 1
print('start idx: %s' % idx)

@app.route('/select', methods=['GET', 'POST'])
def select_option():
    data = json.loads(request.data)
    # First call
    if 'query_id' not in data:
        return 'None'
    query_id = data['query_id']
    option = data['option']
    saved[query_id] = int(option)
    return "None"


@app.route('/save', methods=['GET', 'POST'])
def save_result():
    print(request)
    fo = open('result.jsonl', 'w')
    cnt = 0
    for ex in exs:
        if ex['query_id'] in saved:
            cnt += 1
            result = {'query_id': ex['query_id'], \
                    'query': ex['query'], 'passage': ex['passage'], \
                    'options':ex['options'], 'option': saved[ex['query_id']] }
            fo.write(json.dumps(result) + '\n')
    print({'count':len(saved), 'remain': len(exs)-len(saved)})
    return jsonify({'count': cnt, 'remain': len(exs)-cnt})


@app.route('/next', methods=['GET', 'POST'])
def nextQuery():
    global idx
    idx += 1
    if idx == len(exs):
        return jsonify({'query': 'no more query', 'passage':"no more passsage"})
    ex = exs[idx]
    if ex['query_id'] in saved:
        ex['option'] = saved[ex['query_id']]
    else:
        ex['option'] = -1
    return jsonify(ex)


@app.route('/last', methods=['GET', 'POST'])
def lastQuery():
    global idx
    idx -= 1
    if idx < 0:
        return jsonify({'query': 'no more previous query', 'passage':'no more passage'})
    ex = exs[idx]
    if ex['query_id'] in saved:
        ex['option'] = saved[ex['query_id']]
    else:
        ex['option'] = -1
    return jsonify(ex)


@app.route('/')
def hello():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5982)

