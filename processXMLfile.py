import xml.etree.ElementTree as ET
import codecs
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import logging
import time

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt = '%H:%M:%S', level=logging.INFO)

#for read file xml
tree = ET.parse('training_corpus/enwiki-20191101-pages-articles-multistream5.xml-p352690p565312')
root = tree.getroot()
path = 'articles-corpus//'
url  = '{http://www.mediawiki.org/xml/export-0.10/}page'
fname = 'need_clean_wiki_corpus/clean_enwiki_20191101_5.txt'

#for clean text
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    logging.info("remove stop words &amp; punctuation, and lemmatize words")
    s_free = " ".join([i for i in doc.lower().split() if i not in stop])
    p_free = ''.join(ch for ch in s_free if ch not in exclude)
    lemm   = " ".join(lemma.lemmatize(word) for word in p_free.split())
    words  = lemm.split()

    logging.info("only take words which are greater than 2 characters")
    cleaned = [word for word in words if len(word) > 2]
    cleaned = ' '.join(cleaned)
    return cleaned

def removeUnneededChraters(article_txt):
    #logging.info("remove text written between double curly braces")
    article_txt = re.sub(r"{{.*}}", "", article_txt)

    #logging.info("remove file attachments")
    article_txt = re.sub(r"\[\[File:.*\]\]", "", article_txt)

    #logging.info("remove Image attachments")
    article_txt = re.sub(r"\[\[Image:.*\]\]", "", article_txt)

    #logging.info("remove unwanted lines starting from special characters")
    article_txt = re.sub(r"\n: \'\'.*", "", article_txt)
    article_txt = re.sub(r"\n!.*", "", article_txt)
    article_txt = re.sub(r"^:\'\'.*", "", article_txt)

    #logging.info("remove non-breaking space symbols")
    article_txt = re.sub(r"&amp;nbsp", "", article_txt)

    #logging.info("remove URLs link")
    article_txt = re.sub(r"http\S+", "", article_txt)

    #logging.info("remove digits from text")
    article_txt = re.sub(r"\d+", "", article_txt)

    #logging.info("remove text written between small braces")
    article_txt = re.sub(r"\(.*\)", "", article_txt)

    #logging.info("remove sentence which tells category of article")
    article_txt = re.sub(r"Category:.*", "", article_txt)

    #logging.info("remove the sentences inside infobox or taxobox")
    article_txt = re.sub(r"\| .*", "", article_txt)
    article_txt = re.sub(r"\n\|.*", "", article_txt)
    article_txt = re.sub(r"\n \|.*", "", article_txt)
    article_txt = re.sub(r".* \|\n", "", article_txt)
    article_txt = re.sub(r".*\|\n", "", article_txt)

    #logging.info("remove infobox or taxobox")
    article_txt = re.sub(r"{{Infobox.*", "", article_txt)
    article_txt = re.sub(r"{{infobox.*", "", article_txt)
    article_txt = re.sub(r"{{taxobox.*", "", article_txt)
    article_txt = re.sub(r"{{Taxobox.*", "", article_txt)
    article_txt = re.sub(r"{{ Infobox.*", "", article_txt)
    article_txt = re.sub(r"{{ infobox.*", "", article_txt)
    article_txt = re.sub(r"{{ taxobox.*", "", article_txt)
    article_txt = re.sub(r"{{ Taxobox.*", "", article_txt)

    #logging.info("remove lines starting from *")
    article_txt = re.sub(r"\* .*", "", article_txt)

    #logging.info("remove text written between angle bracket")
    article_txt = re.sub(r"<.*>", "", article_txt)

    #logging.info("remove new line character")
    article_txt = re.sub(r"\n", "", article_txt)

    #logging.info("replace all punctuations with space")
    article_txt = re.sub(
        r"\!|\"|\#|\$|\%|\&amp;|\'|\(|\)|\*|\+|\,|\-|\/|\:|\;|\|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~", " ",
        article_txt)

    #logging.info("replace consecutive multiple space with single space")
    article_txt = re.sub(r" +", " ", article_txt)

    #logging.info("replace non-breaking space with regular space")
    article_txt = article_txt.replace(u'\xa0', u' ')
    return article_txt

t1 = time.time()
with open(fname, 'w') as f:
    for i, page in enumerate(root.findall(url)):
        for p in page:
            r_tag = "{http://www.mediawiki.org/xml/export-0.10/}revision"
            if p.tag == r_tag:
                for x in p:
                    tag = "{http://www.mediawiki.org/xml/export-0.10/}text"
                    if x.tag == tag:
                        text = x.text
                        if not text == None:
                            # Extracting the text portion from the article
                            logging.info("Extracting the text portion from the article")
                            text = text[:text.find("==")]
                            text = removeUnneededChraters(text)
                            logging.info("Writing text to file")
                            f.write(text)

    f.close()

print("Time to make file: ", time.time() - t1)


