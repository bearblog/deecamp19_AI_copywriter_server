#coding=utf-8
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers


es = Elasticsearch([{'host':'10.112.129.228','port':9200}])
import codecs
path = "./new_data.txt"
data_file = codecs.open(path, "r", "utf-8")
values = data_file.readlines()
es.indices.create(index='deecamp_long_gongneng', ignore=400)
actions = []
print("es数据库建立")
for i in range(len(values)):
    line = values[i].split("\t")
    aspect = line[0]
    key = line[1]
    value = line[2].strip()
    length_res = len(value)
    if length_res>95 and aspect == 'c':
        action = {
            "_index":"deecamp_long_gongneng",
            "_type":"keyword_ad",
            "_id":i,
            "_source":{
                "keyword":key,
                'message':value,
            }
        }
        actions.append(action)
    if(len(actions)==500):
        helpers.bulk(es, actions)
        del actions[0:len(actions)]
if (len(actions) > 0):
    helpers.bulk(es, actions)
