import multiprocessing
from gensim.models import Word2Vec
from time import time
import utils

import logging
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

# Read sentences from file
logging.info("Start load sentences from file")
fname = "word2vec_data/Bigram_enwiki_corpus_1.txt"
sentences = utils.read(fname)


logging.info("Count the number of cores in this computer")
cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# Train
min_count = 5
window = 5
size = 200
sample = 1e-3
alpha = 0.01
min_alpha = 1e-5
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
                     workers=cores-1)

t = time()

w2v_model.build_vocab(sentences=sentences, progress_per=10000)
print('Time to build vocab: {} mins'.format(round(time() - t) / 60, 2))

t = time()

#w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1, compute_loss=True)

print('Time to train the model: {} mins'.format(round(time() - t) / 60, 2))


print(w2v_model.get_latest_training_loss())
#w2v_model.save("trained_model/bigrams.model")
w2v_model.init_sims(replace=True)

logging.info("\n")

