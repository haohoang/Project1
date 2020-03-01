from nltk.tokenize import sent_tokenize
import utils
import logging
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

with open("clean_enwiki_1.txt",'r', encoding = 'latin_1') as f:
    data = f.read()

#  to sentences:
sentences = sent_tokenize(data)
print(sentences[:3])
# distint word:
for i, sent in enumerate(sentences):
    if i % 1000 ==0 :
        logging.info("PROCESS {0} sentences.".format(i))
    sentences[i] = utils.clean_remain_tag(sent)

print(sentences[:10])

# Write and save file
fname = "pog_tag_enwiki.txt"
utils.save(fname, sentences)



