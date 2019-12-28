import time
from contextlib import contextmanager
from elasticsearch import Elasticsearch
# Elasticsearch

# 连接ES服务
def connet_elasticsearch(host, port):
    _es = None
    _es = Elasticsearch([{'host': host, 'port': port}])
    if _es.ping():
        print("[Elasticsearch]Successfully connected")
    else:
        print("[Elasticsearch]Wow something is wrong! Bad connection!")
    return _es

es = connet_elasticsearch("10.112.57.93", 9200)

def keywords_search(keywords,num,length,aspects):
    keywords_list, description_list = [],[]
    # body={"query":{"match_all":{}}}
    body={'query': {'match': {'keyword': keywords}}, 'size':num}
    if aspects == '1' or aspects == 'a':
        aspects = 'waiguan'
    elif aspects == '2' or aspects == 'b':
        aspects = 'caizhi'
    elif aspects == '3' or aspects == 'c':
        aspects = 'gongneng'
    else:
        aspects = 'waiguan'

    if length == 'a':
        length = 'short'
    elif length == 'b':
        length = 'mid'
    elif length == 'c':
        length = 'long'
    else:
        length = 'short'
    result = es.search("deecamp_"+length+'_'+aspects, body)
    for tmp in result["hits"]["hits"]:
        keywords_list.append(tmp['_source']['keyword'])
        description_list.append(tmp['_source']['message'])
    return keywords_list, description_list

def muti_search(keywords,num,length):
    keywords_list, description_list = [],[]
    # body={"query":{"match_all":{}}}
    body={'query': {'match': {'keyword': keywords}}, 'size':num}
    result = es.search("sku_long", body)
    for tmp in result["hits"]["hits"]:
        keywords_list.append(tmp['_source']['keyword'])
        description_list.append(tmp['_source']['message'])
    return keywords_list, description_list





