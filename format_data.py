#!/usr/bin/env python
# coding: utf-8

import json
import random
import ipdb

data = json.load(open('dev-v2.0.json'))
fo = open('test.jsonl', 'w')
cnt = 30
results = []
for wiki in data['data']:
    for para in wiki['paragraphs']:
        for qa in para['qas']:
            results.append({'passage': para['context'], 'query': qa['question'], 'query_id': qa['id'], 'options':['Negation','Antonym','Entity Swap','Mutual Exclusion',\
                    'Impossible Condition','Other Neutual','Answerable']})
for res in random.sample(results, cnt):
    fo.write(json.dumps(res) + '\n')
