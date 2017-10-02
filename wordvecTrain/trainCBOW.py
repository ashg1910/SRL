from gensim.models import Word2Vec,word2vec
from  sys import stdin
import cPickle as pickle
import os
import logging
import sys
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 

class MySentences(object):
  def __init__(self, dirname):
    self.dirname = dirname

  def __iter__(self):
    for fname in os.listdir(self.dirname):
      for line in open(os.path.join(self.dirname, fname)):
        yield line.decode('utf8').split()

#sentences = MySentences('./split_W/')
filename = sys.argv[1]
sentences = MySentences(filename)

#sentences = []
#for i in stdin:
#  sentences.append(i)
  
model = Word2Vec(sentences, size=30, window=10 , min_count=1, sg = 0)

#model.save("clean_w2v.txt")
model.save("hindi_model.txt")

#vocab = list(model.vocab.keys())
#print vocab
