from gensim.models import Word2Vec
import logging

logging.basicConfig(level=logging.INFO)

model = Word2Vec.load('wiki.model')

accuracy = model.accuracy("questions-words.txt")
print(model.wv.most_similar('girl'))
print(model.wv.most_similar('boy'))
print(model.wv.most_similar('king'))
print(model.wv.most_similar('country'))
for sec in accuracy:
    print(sec['incorrect'])
