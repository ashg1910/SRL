import codecs
from gensim.models import Word2Vec,word2vec
from  sys import stdin
import cPickle as pickle
import os
import logging
import sys
import numpy as np
from sklearn import linear_model, svm
np.random.seed(123)
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors
from sklearn.preprocessing import Normalizer

from keras.models import Sequential
from keras.layers import Merge
from keras.layers.core import Dense, Activation, Reshape
from keras.layers.embeddings import Embedding
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical

vectorFile1 = './vectorToTrain.npy'
vectorFile2 = './allTest/vectorToTest.npy'

trainVectors = np.load(vectorFile1)
testVectors = np.load(vectorFile2)
# trainVectors = trainVectors[:100]
# testVectors = testVectors[:100]
allVecs = np.concatenate((trainVectors, testVectors), axis=0)

arguments = pickle.load(open("../arguments.p","rb"))
total = 0
correct = 0
results = [[0]*22 for _ in range(22)]
support = [0]*22
argIdResult = [[0]*3 for _ in range(3)]

for i in range(5, 6):
    x = len(allVecs) * 0.2 * (i-1)
    n = len(allVecs) * 0.2 * i
    testData = allVecs[x:n]
    trainData = []
    for j in range(0, len(allVecs)) :
        if j<x or j>=n :
            trainData.append(allVecs[j])
    trainData = np.array(trainData)
    testData = np.array(testData)

    indata = []
    outdata = []

    for vec in trainData :
        indata.append(vec[:-2])
        outdata.append(vec[-1])

    clf = svm.SVC(C=60.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, 
        class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovo', random_state=None)
    clf.fit(indata, outdata)


    for vec in testData :
        
        total += 1
        #kSVM
        predictedVal = int(clf.predict(vec[:-2].reshape(1,-1)))

        actualVal = int(vec[-1])
        support[actualVal] += 1

        if predictedVal == actualVal :
            correct += 1

        results[predictedVal][actualVal] += 1
        
        if actualVal > 1 :
            actualVal = 2
        if predictedVal > 1 :
            predictedVal = 2
        
        argIdResult[predictedVal][actualVal] += 1

print support[1], sum(support)-support[1]

print "ARG Identify Results :-"
id_p, id_r, id_f = float(0), float(0) , float(0)
for i in range(2) :
    tp = float(argIdResult[i+1][i+1])
    fp = float(sum(argIdResult[i+1]) - tp)
    fn = float(sum(row[i+1] for row in argIdResult) - tp)
    # print tp, fp, fn
    precision = float(0)
    recall = float(0)
    f_score = float(0)
    if tp != 0 :
        precision = float(tp/float(tp+fp))
        recall = float(tp/float(tp+fn))
        if precision!=0 and recall!=0 :
            f_score = 2 * (precision*recall) / (precision+recall)
    print "Class",i,":", precision, recall, f_score
    if i==0 :
        print "Support: ", support[1]/5
        id_p += precision * support[1]
        id_r += recall * support[1]
        id_f += f_score * support[1]
    if i==1 :
        print "Support: ", (sum(support) - support[1] )/5
        id_p += precision * (sum(support) - support[1] )
        id_r += recall * (sum(support) - support[1] )
        id_f += f_score * (sum(support) - support[1] )

id_p = id_p/(sum(support))
id_r = id_r/(sum(support))
id_f = id_f/(sum(support))
print "AVG: ", id_p, id_r, id_f
print "\n"

avg_p, avg_r, avg_f = float(0), float(0) , float(0)
all_p, all_r, all_f = float(0), float(0) , float(0)
for i in range(len(arguments)):
    tp = float(results[i+1][i+1])
    fp = float(sum(results[i+1]) - tp)
    fn = float(sum(row[i+1] for row in results) - tp)
    precision = float(0)
    recall = float(0)
    f_score = float(0)
    if tp != 0 :
        precision = float(tp/float(tp+fp))
        recall = float(tp/float(tp+fn))
        if precision!=0 and recall!=0 :
            f_score = 2 * (precision*recall) / (precision+recall)
    print arguments[i], ":", precision, recall, f_score, support[i+1]/5
    
    if i>0:
        avg_p += precision*support[i+1]
        avg_r += recall*support[i+1]
        avg_f += f_score*support[i+1]

    all_p += precision*support[i+1]
    all_r += recall*support[i+1]
    all_f += f_score*support[i+1]


avg_p = avg_p/(sum(support) - support[1])
avg_r = avg_r/(sum(support) - support[1])
avg_f = avg_f/(sum(support) - support[1])

all_p = all_p/(sum(support))
all_r = all_r/(sum(support))
all_f = all_f/(sum(support))

print "AVG: ", avg_p, avg_r, avg_f
print "\n"

print "AVG: ", all_p, all_r, all_f
print "Accuracy: ", float(float(correct)/float(total)) * 100

