from __future__ import division
from collections import defaultdict
from math import log
from copy import deepcopy

sentences = []
fname = 'need_clean_wiki_corpus/clean_brown(1).txt'
with open(fname, 'r', encoding='utf-8') as f:
    while True:
        sent = f.readline()
        if len(sent) == 0:
            break
        sent = sent[:-1].split()
        sentences.append(sent)
    f.close()

def countUnigram(sentences):
  total_word_count = 0
  unigram_vocab = defaultdict(int)
  for sent in sentences:
    for i in sent:
      unigram_vocab[i] += 1
      total_word_count += 1
  return unigram_vocab, total_word_count

def countBigram(sentences):
  bigram_vocab = defaultdict(int)
  for sent in sentences:
    for i in range(len(sent) - 1):
      temp = sent[i] + "_" + sent[i+1]
      bigram_vocab[temp] += 1
  return bigram_vocab

def score(word_a, word_b, word_ab, total_word_count):
  pa = float(word_a) / float(total_word_count)
  pb = float(word_b) / float(total_word_count)
  pab = float(word_ab) / float(total_word_count)
  npmi = log(pab / (pa * pb)) / -log(pab)
  return npmi

def buildBigramVocab(unigram_vocab, bigram_vocab, total_word_count, mint_count = 5, threshold = 0.1):
  new_bigram_vocab = list()
  for word, count in bigram_vocab.items():
    if count >= mint_count:
      temp = word.split("_")
      word_a = temp[0]
      word_b = temp[1]
      npmi = score(unigram_vocab[word_a], unigram_vocab[word_b], count, total_word_count)
      if npmi >= threshold:
        new_bigram_vocab.append(word)
  return new_bigram_vocab

def identifyBigram(sentences, bigram_vocab):
  new_sentences = deepcopy(sentences)
  for i, sent in enumerate(new_sentences):
    if i % 1000 == 0:
      print("Process {0} sentences".format(i))
    new_sent = []
    j = 0
    while j < (len(sent) - 1):
      temp = sent[j] + "_" + sent[j+1]
      if temp in bigram_vocab:
        new_sent.append(temp)
        j += 1
        if j == len(sent) - 2:
          new_sent.append(sent[j+1])
      else:
        new_sent.append(sent[j])
        if j == len(sent) - 2:
          new_sent.append(sent[j+1])
      j += 1
    new_sentences[i] = new_sent
  return new_sentences


unigram_vocab, total_word_count = countUnigram(sentences)

bigram_vocab = countBigram(sentences)
bigram_vocab = buildBigramVocab(unigram_vocab, bigram_vocab, total_word_count, mint_count = 1, threshold = 0.1)
print(bigram_vocab)

new_sentences = identifyBigram(sentences, bigram_vocab)


#Save to file
fname = 'Bigram_brown_npmi(2).txt'
with open(fname,'w',encoding = 'utf-8') as f:
    for sent in new_sentences:
        for i in sent:
            f.write("%s " % i)
        f.write('\n')
    f.close()
