import logging
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from collections import  defaultdict # For word frequency
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import multiprocessing
from gensim.models import Word2Vec
from time import time
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    # tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    # tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append([word.lower(), tag])
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append([lemmatizer.lemmatize(word, tag).lower(), tag])
    return lemmatized_sentence

def clean(doc):

    lemm = lemmatize_sentence(doc)
    s_free = [i for i in lemm if i[0] not in stop]
    p_free = []
    for word in s_free:
      new_word = []
      for ch in word[0]:
        if ch not in exclude:
          new_word.append(ch)
      new_word = "".join(new_word)
      word1 = new_word + "_" + str(word[1])
      if(len(new_word) > 2):
        p_free.append(word1)
    return p_free

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
with open("lee_background.cor.txt","r") as f:
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
fname = "clean_lee_background.cor.txt"
with open(fname,'w',encoding = 'utf-8') as f:
    for sent in sentences:
        for i in sent:
            f.write("%s " % i)
        f.write('\n')

print(len(sentences))
