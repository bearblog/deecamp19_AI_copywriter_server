from gensim.models import word2vec
import jieba
from bert_serving.client import BertClient

bc = BertClient()
print('BERT模型加载成功')
model_word2vec = word2vec.Word2Vec.load('pretrain_model/word2vec_model/sku_word2vec.model')
print('word2vec模型加载成功')


def edit_sentence(now_keywords, raw_sentence):
    now_keys = now_keywords.split()
    raw_sen = jieba.lcut(raw_sentence)
    for tmp1 in now_keys:
        for tmp2 in raw_sen:
            try:
                if model_word2vec.wv.similarity(tmp1, tmp2) > 0.6:
                    raw_sen[raw_sen.index(tmp2)] = tmp1
            except KeyError:
                continue
    return ''.join(raw_sen)


def cosine_similarity(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return round(dot_product / ((normA ** 0.5) * (normB ** 0.5)), 4)


def get_bert_result(keywords, description_list):
    try:
        all_list = [keywords] + description_list
        bert_scores = bc.encode(all_list)
        res_scores = {}
        res_list = []
        for i in range(1, len(bert_scores)):
            score = cosine_similarity(bert_scores[0], bert_scores[i])
            res_scores[description_list[i - 1]] = score
        score_sort = sorted(res_scores.items(), key=lambda x: x[1], reverse=True)
        for value, _ in score_sort:
            res_list.append(value)
        return res_list
    except:
        return description_list
