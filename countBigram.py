from gensim.models import Word2Vec
import logging

logging.basicConfig(level=logging.INFO)

model = Word2Vec.load('trained_model/phrases_enwiki.model')

print(model.wv.most_similar("city"))
