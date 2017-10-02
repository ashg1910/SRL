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

class Model(object):

    def evaluate(self, X_val, y_val):
        correct = 0
        output = []
        for i in range(len(X_val)) :
            output.append(self.guess(X_val[i].reshape(1,-1)))
        for i in range(len(output)):
            outClass = output[i].argmax()
            actualClass = y_val[i].argmax()

            if outClass == actualClass :
                correct += 1

        return (correct*100)/len(output)


class NN(Model):

    def __init__(self, X_train, y_train, X_val, y_val, dim):
        super(NN, self).__init__()
        self.dim = dim
        self.nb_epoch = 15
        self.checkpointer = ModelCheckpoint(filepath="best_model_weights.hdf5", verbose=1, save_best_only=True)
        # self.max_log_y = max(numpy.max(numpy.log(y_train)), numpy.max(numpy.log(y_val)))
        self.__build_keras_model()
        self.fit(X_train, y_train, X_val, y_val)

    def __build_keras_model(self):
        l1 = self.dim
        self.model = Sequential()
        self.model.add(Dense(l1, init='uniform', input_dim=self.dim))
        self.model.add(Activation('relu'))
        # self.model.add(Dense(l1/2, init='uniform'))
        # self.model.add(Activation('relu'))
        # self.model.add(Dense(l1/4, init='uniform'))
        # self.model.add(Activation('relu'))
        self.model.add(Dense(22))
        # self.model.add(Activation('sigmoid'))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        # self.model.compile(loss='mean_absolute_error', optimizer='adam')

    def _val_for_fit(self, val):
        val = numpy.log(val) / self.max_log_y
        return val

    def _val_for_pred(self, val):
        return numpy.exp(val * self.max_log_y)

    def fit(self, X_train, y_train, X_val, y_val):
        self.model.fit(X_train, y_train,
                       validation_data=(X_val, y_val),
                       nb_epoch=self.nb_epoch 
                       # batch_size=128,
                       # callbacks=[self.checkpointer],
                       )
        # self.model.load_weights('best_model_weights.hdf5')
        print "Result on validation data: ", self.evaluate(X_val, y_val)

        model_json = self.model.to_json()
        with open("NN_model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights("NN_model.h5")
        print("Saved model to disk")

    def guess(self, features):
        # result = self.model.predict(features).flatten()
        # return self._val_for_pred(result)
        result = self.model.predict(features)
        return result



vectorFile = sys.argv[1]

trainVectors = np.load(vectorFile)

indata = []
outdata = []

for vec in trainVectors :
    indata.append(vec[:-2])
    outdata.append(vec[-1])

# indata = np.array(indata)
# outdata = np.array(outdata)
# outdata = to_categorical(outdata)

val_x = indata[:100]
val_y = outdata[:100]

input_dim = len(indata[0])

# model = NN(indata, outdata, val_x, val_y, input_dim)

clf = svm.SVC(C=60.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, 
    class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovo', random_state=None)
clf.fit(indata, outdata)
pickle.dump(clf, open('SVC_Model','w'))