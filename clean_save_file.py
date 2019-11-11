from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from collections import  defaultdict # For word frequency

import logging # Setting upp the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

def clean(doc):
    #logging.info("remove stop words &amp; punctuation, and lemmatize words")
    s_free = " ".join([i for i in doc.lower().split() if i not in stop])
    p_free = ''.join(ch for ch in s_free if ch not in exclude)
    lemm   = " ".join(lemma.lemmatize(word) for word in p_free.split())
    words  = lemm.split()
    #logging.info("only take words which are greater than 2 characters")
    cleaned = [word for word in words if len(word) > 2]
    return cleaned

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

with open("need_clean_wiki_corpus/clean_enwiki_20191101_5.txt","r") as f:
    data = f.read()
    f.close()
#  to sentences:
sentences = sent_tokenize(data)
print(sentences[:3])
# distint word:
for i, sent in enumerate(sentences):
    if i % 1000 ==0 :
        logging.info("PROCESS {0} sentences.".format(i))
    sentences[i] = clean(sent)

# Save to
fname = "clean_wiki_corpus.txt"
with open(fname,'a',encoding = 'utf-8') as f:
    for sent in sentences:
        for i in sent:
            f.write("%s " % i)
        f.write('\n')

print(len(sentences))
word_freq = defaultdict(int)
for sent in sentences:
    for i in sent:
        word_freq[i] += 1
print(len(word_freq))
sorted(word_freq, key=word_freq.get, reverse=True)[:10]


