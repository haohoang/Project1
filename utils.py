import nltk
import ssl
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from string import punctuation


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


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

# Write and save file
def save(fname, sentences):
    with open(fname, 'w', encoding='utf-8') as f:
        for sent in sentences:
            for i in sent:
                f.write("%s " % i)
            f.write('\n')

# Read file
def read(fname):
    sentences = []
    with open(fname, 'r', encoding='utf-8') as f:
        while True:
            sent = f.readline()
            if len(sent) == 0:
                break
            sent = sent[:-1].split()
            sentences.append(sent)
    return sentences