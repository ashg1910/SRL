import ssfAPI
from sklearn.metrics import classification_report
import codecs
from gensim.models import Word2Vec,word2vec
from  sys import stdin
import cPickle as pickle
import os
import logging
import sys
import numpy as np
from sklearn import linear_model, svm
from keras.models import model_from_json


vectorFile = sys.argv[1]

f = open("./allTest/testFeats.txt")
testFeats = f.readlines()
testVectors = np.load(vectorFile)

arguments = pickle.load(open("../arguments.p","rb"))

outFile = open('outliers.txt','w')
errorSentences = []

total = 0
correct = 0
x = []
y = []

clf = pickle.load(open("./SVC_Model","rb"))

json_file = open('NN_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("NN_model.h5")
print("Loaded model from disk")

#testVectors = testVectors[:100]

results = [[0]*22 for _ in range(22)]
support = [0]*22
argIdResult = [[0]*3 for _ in range(3)]
for vec in testVectors :
	
	total += 1
	#kSVM
	predictedVal = int(clf.predict(vec[:-2].reshape(1,-1)))

	# #NN model
	# output = loaded_model.predict(vec[:-2].reshape(1,-1))
	# predictedVal = output[0].argmax()

	actualVal = int(vec[-1])
	support[actualVal] += 1

	if predictedVal == actualVal :
		correct += 1

	if predictedVal != actualVal :
		uid = vec[-2]
		feats = testFeats[int(uid)-1]
		outFile.write(feats)
		outFile.write(str(arguments[predictedVal-1]))
		outFile.write('\n')
		if feats not in errorSentences :
			errorSentences.append(feats)

	# if actualVal != 1 :
	x.append(actualVal)
	y.append(predictedVal)
	results[predictedVal][actualVal] += 1
	if actualVal > 1 :
		actualVal = 2
	if predictedVal > 1 :
		predictedVal = 2
	argIdResult[predictedVal][actualVal] += 1

# report = classification_report(x, y)
# print report
# print results
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
		id_p += precision * support[1]
		id_r += recall * support[1]
		id_f += f_score * support[1]
	if i==1 :
		id_p += precision * (sum(support) - support[1] )
		id_r += recall * (sum(support) - support[1] )
		id_f += f_score * (sum(support) - support[1] )

id_p = id_p/(sum(support))
id_r = id_r/(sum(support))
id_f = id_f/(sum(support))
print "AVG: ", id_p, id_r, id_f
print "\n"

avg_p, avg_r, avg_f = float(0), float(0) , float(0)
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
	print arguments[i], ":", precision, recall, f_score
	
	if i>0:
		avg_p += precision*support[i+1]
		avg_r += recall*support[i+1]
		avg_f += f_score*support[i+1]

avg_p = avg_p/(sum(support) - support[1])
avg_r = avg_r/(sum(support) - support[1])
avg_f = avg_f/(sum(support) - support[1])
print "\n"
print "AVG: ", avg_p, avg_r, avg_f
	
print "Accuracy: ", float(float(correct)/float(total)) * 100

outFile.write("\n\n")

# for sent in errorSentences :
# 	outFile.write(sent)
# 	sent = sent.split(' ')[17]
# 	sent = sent.split(',')
# 	d = ssfAPI.Document('../Test/'+ sent[0])
# 	for tree in d.nodeList :
# 		if tree.name == sent[1] :
# 			string = ""
# 			string += "<Sentence id='" + sent[1] + "'>"
# 			string += tree.text
# 			string += "</Sentence>\n\n"
# 			u = string.encode("utf-8")
# 			outFile.write(u)

outFile.close()

f.close()