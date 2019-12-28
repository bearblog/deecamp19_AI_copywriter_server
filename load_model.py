from KOBE_model.core.api_a import *
import torch
from gensim.models import word2vec

keywords_list = []
with open('data/keywords_150.txt',encoding = 'utf-8')as f:
    data = f.readlines()
for tmp in data:
    keywords_list.append(tmp.strip())
model_short = DescriptionGenerator(
    config="KOBE_model/configs/small.yaml",
    gpu="0",
    restore=False,
    pretrain="KOBE_model/experiments/model/short/best_bleu_checkpoint.pt",
    mode="eval",
    batch_size=1,
    beam_size=6,
    scale=1,
    char=False,
    use_cuda=True,
    seed=1234,
    model="tensor2tensor",
    num_workers=0
)
print('short model load success!!!')
model_mid = DescriptionGenerator(
    config="KOBE_model/configs/small.yaml",
    gpu="0",
    restore=False,
    pretrain="KOBE_model/experiments/model/mid/best_bleu_checkpoint.pt",
    mode="eval",
    batch_size=1,
    beam_size=6,
    scale=1,
    char=False,
    use_cuda=True,
    seed=1234, 
    model="tensor2tensor",
    num_workers=0
)
print('mid model load success!!!')
model_long = DescriptionGenerator(
    config="KOBE_model/configs/small.yaml",
    gpu="0",
    restore=False,
    pretrain="KOBE_model/experiments/model/long/best_bleu_checkpoint.pt",
    mode="eval",
    batch_size=1,
    beam_size=6,
    scale=1,
    char=False,
    use_cuda=True,
    seed=1234,
    model="tensor2tensor",
    num_workers=0
)
print('long model load success!!!')
keywords_word2vec = word2vec.Word2Vec.load('pretrain_model/word2vec_model/keys_word2vec.model')