import nltk
import ssl
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from string import punctuation
import logging
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)


"""try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')"""

stop = set(stopwords.words('english'))
exclude = set(punctuation)

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

# POS_TAG
def lemmatize_sentence_remain_tag(sentence):
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

def clean_remain_tag(doc):
    lemm = lemmatize_sentence_remain_tag(doc)
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

# Bigram
def clean_not_remain_tag(doc):
    #remove stop words, punctuation, and lemmatize words
    lemm   = lemmatize_sentence_not_retain_tag(doc)
    s_free = " ".join([i for i in lemm if i not in stop])
    p_free = ''.join([ch for ch in s_free if ch not in exclude])
    #only take words which are greater than 2 characters"
    cleaned = [word for word in p_free.split() if len(word) > 2]
    return cleaned

def lemmatize_sentence_not_retain_tag(sentence):
    lemmatizer = WordNetLemmatizer()
    #tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    #tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            #if there is no available tag, append the token as is
            lemmatized_sentence.append(word.lower())
        else:
            #else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word.lower(), tag))
    return lemmatized_sentence

def sent2Bigram(sent):
    new_sent = []
    new_sent.append('b_' + sent[0])
    for i in range(len(sent)):
        if i == len(sent) - 1:
            temp = sent[i] + "_e"
        else:
            temp = sent[i] + "_" + sent[i+1]
        new_sent.append(temp)
    return new_sent

# Write and save file
def save(fname, sentences):
    with open(fname, 'w', encoding='utf-8') as f:
        for j, sent in enumerate(sentences):
            if j % 1000 == 0:
                logging.info("Write %d sentences", j)
            for i in sent:
                f.write("%s " % i)
            f.write('\n')

# Read file
def read(fname):
    sentences = []
    i = 0
    with open(fname, 'r', encoding='utf-8') as f:
        while True:
            if i % 1000 == 0:
                logging.info("Read %d sentences", i)
            i += 1
            sent = f.readline()
            if len(sent) == 0:
                break
            sent = sent[:-1].split()
            sentences.append(sent)
    return sentences