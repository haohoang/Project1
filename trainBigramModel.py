import multiprocessing
from gensim.models import Word2Vec
from time import time
import logging # Setting upp the loggings to monitor gensim
import utils
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)


# Read sentences from file
logging.info("Start load sentences from file")
fname = "Bigram_enwiki_corpus_1.txt"
sentences = utils.read(fname)

logging.info("Count the number of cores in this computer")
cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# Train
min_count = 10
window = 5
size = 200
sample = 1e-3
alpha = 0.03
min_alpha = 1e-7
negative = 5
hs = 0
sg = 0
logging.info("Start training with min_count={0}, window={1}, size={2}, sample={3}, alpha={4}, min_alpha={5}, negative={6}. sg={7}, hs={8}"
             .format(min_count, window, size, sample, alpha, min_alpha, negative, sg, hs))
bigram_model = Word2Vec(min_count=min_count,
                     sg = sg,
                     hs=hs,
                     window=window,
                     seed= 42,
                     size=size,
                     sample=sample,
                     alpha=alpha,
                     min_alpha=min_alpha,
                     negative=negative,
                     compute_loss= True,
                     workers=cores-1)

t = time()

bigram_model.build_vocab(sentences=sentences, progress_per=10000)
print('Time to build vocab: {} mins'.format(round(time() - t) / 60, 2))

t = time()

bigram_model.train(sentences, total_examples=bigram_model.corpus_count, epochs=10, report_delay=1)

print('Time to train the model: {} mins'.format(round(time() - t) / 60, 2))

print(bigram_model.get_latest_training_loss())
bigram_model.save("trained_model/Bigram_wiki_corpus_1.model")
bigram_model.init_sims(replace=True)


print(bigram_model.similarity("come_true", "dream_come"))
logging.info("\n")
for i, word in enumerate(bigram_model.wv.vocab):
    if i == 10:
        break
    print(word)
