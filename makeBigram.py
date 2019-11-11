from time import time
import logging
from gensim.test.utils import datapath
from gensim.models import Word2Vec
from gensim import utils
import multiprocessing
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

class MyCorpus(object):
    def __iter__(self):
        corpus_path = datapath('lee_background.cor')
        for line in open(corpus_path):
            yield utils.simple_preprocess(line)

def sent2Bigram(sent):
    for i in range(len(sent)-1):
        sent[i] = sent[i] + "_" + sent[i+1]

sentences = []
fname = 'clean_wiki_corpus.txt'
with open(fname, 'r', encoding='utf-8') as f:
    while True:
        sent = f.readline()
        if len(sent) == 0:
            break
        sent = sent[:-1].split()
        sent2Bigram(sent)
        sentences.append(sent)
    f.close()

fname = 'Bigram_wiki_corpus.txt'
with open(fname,'a',encoding = 'utf-8') as f:
    for sent in sentences:
        for i in sent:
            f.write("%s " % i)
        f.write('\n')
    f.close()

logging.info("Count the number of cores in this computer")
cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# Train
min_count = 1
window = 5
size = 200
sample = 1e-3
alpha = 0.03
min_alpha = 0.0007
negative = 5
hs = 0
sg = 0
logging.info("Start training with min_count={0}, window={1}, size={2}, sample={3}, alpha={4}, min_alpha={5}, negative={6}. sg={7}, hs={8}"
             .format(min_count, window, size, sample, alpha, min_alpha, negative, sg, hs))
w2v_model = Word2Vec(min_count=min_count,
                     sg = sg,
                     hs=hs,
                     window=window,
                     size=size,
                     sample=sample,
                     alpha=alpha,
                     min_alpha=min_alpha,
                     negative=negative,
                     compute_loss=False,
                     workers=cores-1)

t = time()

w2v_model.build_vocab(sentences=sentences, progress_per=10000)
print('Time to build vocab: {} mins'.format(round(time() - t) / 60, 2))

t = time()

w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=10, report_delay=1)

print('Time to train the model: {} mins'.format(round(time() - t) / 60, 2))


#print(w2v_model.score(sentences=sentences, total_sentences=len(sentences)))
w2v_model.save("wiki.model")
w2v_model.init_sims(replace=True)

logging.info("\n")
print(w2v_model.wv.vocab[:10])