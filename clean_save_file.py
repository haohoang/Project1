import nltk
import ssl
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from string import punctuation
import logging
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

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


lemmatizer = WordNetLemmatizer()

# function to convert nltk tag to wordnet tag
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

def clean(doc):
    #remove stop words &amp; punctuation, and lemmatize words
    lemm   = lemmatize_sentence(doc)
    s_free = " ".join([i for i in lemm if i not in stop])
    p_free = ''.join([ch for ch in s_free if ch not in exclude])
    #only take words which are greater than 2 characters"
    cleaned = [word for word in p_free.split() if len(word) > 2]
    return cleaned

stop = set(stopwords.words('english'))
exclude = set(punctuation)

with open("need_clean_wiki_corpus/clean_simplewiki_20170201.txt","r") as f:
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
fname = "clean_wiki_copus(1).txt"

with open(fname,'a',encoding = 'utf-8') as f:
    for sent in sentences:
        for i in sent:
            f.write("%s " % i)
        f.write('\n')

print(len(sentences))



