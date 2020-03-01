import utils
import logging
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

sentences = []
fname = 'cleaned-enwiki_1.txt'
with open(fname, 'r', encoding='utf-8') as f:
    i=0
    while True:
        i += 1
        if i%1000 == 0:
            logging.info("PROCESS {0} sentences".format(i))
        sent = f.readline()
        if len(sent) == 0:
            break
        elif 0 < len(sent) <= 2:
            continue
        sent = sent[:-1].split()
        sent = utils.sent2Bigram(sent)
        sentences.append(sent)

#Save to file
fname = 'Bigram_enwiki_corpus_1.txt'
utils.save(fname, sentences)




