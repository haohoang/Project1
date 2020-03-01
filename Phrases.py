from gensim.models.phrases import Phrases
import utils
import logging
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

sentences = utils.read("word2vec_data/cleaned-enwiki_1.txt")

bigram = Phrases(sentences, min_count=1, threshold=0.7, scoring="npmi")

sentences = list(bigram[sentences])

utils.save("word2vec_data/Phrases.txt", sentences)

