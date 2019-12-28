from flask import Flask, request, jsonify
from flask_cors import CORS
from ES_model.ES_search import *
from ES_model.dataprocess import *
import json
import random
import logging
import jieba
import random
from pretrain_model.wds import *
from load_model import *

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
stopwords = ['www', '桔子折特卖', '领券', '链接', '独家券', '包邮', 'com', 'br', '红包']


@app.route('/deecamp')
def input():
    keywords = request.args.get('keywords', type=str)
    aspects = request.args.get('aspects', type=str)
    length = request.args.get('length', type=str)
    app.logger.info('keywords: ' + str(keywords) + ' aspects: ' + str(aspects) + ' length: ' + str(length))
    if keywords is None or keywords == '' or keywords.replace(' ', '') == '':
        result = ['please input your keywords' for _ in range(4)]
    else:
        replay = []
        keywords_reslist, message_reslist = keywords_search(keywords, 4, length, aspects)
        kobe_res = get_longchoose_kobe(keywords, aspects, length)
        replay.append(edit_sentence(keywords, kobe_res.strip()))
        new_es = []
        for i in range(len(message_reslist)):
            replay.append(edit_sentence(keywords, message_reslist[i].strip()))
        for sentence in replay:
            flag = 1
            num = 0
            for stopword in stopwords:
                if stopword in sentence:
                    flag = 0
            for tmp in sentence:
                if tmp.isdigit():
                    num += 1
            if flag == 1 and num < 15:
                new_es.append(sentence)
        result = get_bert_result(keywords, new_es)
    app.logger.info('/t'.join(result))
    if len(result) >= 4:
        return jsonify(result[:4])
    else:
        return jsonify(result)


@app.route('/deecamp_keywords')
def input_keywords():
    return jsonify(keywords_list)


@app.route('/deecamp_muti')
def get_muti():
    keywords = request.args.get('keywords', type=str)
    if keywords == '':
        replay = ['please input your keywords!']
    else:
        replay = []
        _, message_reslist = muti_search(keywords, 15, 'c')
        for line in message_reslist:
            lines = line.strip().replace('。', '，').replace('！', '，').replace('？', '，').split('，')
            for tmp in lines:
                muti_flag = 1
                for stopword in stopwords:
                    if stopword in tmp:
                        muti_flag = 0
                if 10 < len(tmp) < 30 and muti_flag == 1:
                    replay.append(tmp)
        random.shuffle(replay)
        if len(replay) > 15:
            replay = replay[:15]
    return jsonify(replay)


@app.route('/deecamp_dynamic')
def get_dynamic_keywords():
    keywords = request.args.get('keywords', type=str)
    if keywords == '' or keywords == ' ':
        replay = ['外套', '衬衫', '裤子', '休闲裤', '男鞋', '牛仔裤', '卫衣', '夹克', '婴儿', '毛衣', '收纳', '沙发', '置物架', '连衣裙', '厨房', '通用',
                  '春秋季', '卫生间', '便携式', '斜挎包', '不粘锅', '小孩', '高档', '笔记本', '吸顶灯', '运动套装', '小学生', '日系', '火锅', '笔记本电脑']
    else:
        ues_word = keywords.strip().split()
        try:
            sim_tuple = keywords_word2vec.most_similar(ues_word[-1], topn=50)
            replay = []
            for tmp in sim_tuple:
                if 0.4 < tmp[1] < 0.6:
                    if tmp[0] not in ues_word:
                        replay.append(tmp[0])
        except:
            replay = ['外套', '衬衫', '裤子', '休闲裤', '男鞋', '牛仔裤', '卫衣', '夹克', '婴儿', '毛衣', '收纳', '沙发', '置物架', '连衣裙', '厨房',
                      '通用', '春秋季', '卫生间', '便携式', '斜挎包', '不粘锅', '小孩', '高档', '笔记本', '吸顶灯', '运动套装', '小学生', '日系', '火锅',
                      '笔记本电脑']
    return jsonify(replay)


def get_longchoose_kobe(keywords, aspects, length):
    if aspects == '1':
        aspects = 'a'
    if aspects == '2':
        aspects = 'b'
    if aspects == '3':
        aspects = 'c'
    dicts = {}
    dicts['src'] = utils.Dict(data='KOBE_model/core/dataloading/src.dict')
    keywords = ' '.join(list(keywords.strip().replace(' ', '')))
    try:
        ids = string2id(keywords.replace(' ', ''), model_CNN)
    except:
        ids = 3
    inputstr = '<' + str(ids) + '> ' + '<' + aspects + '> ' + keywords
    srcIds = dicts['src'].convertToIdx(inputstr.split(), utils.UNK_WORD)
    try:
        if length == 'a':
            return "".join('%s' % ids for ids in model_short.predict(srcIds))
        elif length == 'b':
            return "".join('%s' % ids for ids in model_mid.predict(srcIds))
        else:
            return "".join('%s' % ids for ids in model_long.predict(srcIds))
    except:
        return "抱歉，这里可能出了点问题..."


if __name__ == '__main__':
    PATH = 'pretrain_model/epoch_54_accuracy_0.781500'
    model_CNN = torch.load(PATH)
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8080, threaded=True)
