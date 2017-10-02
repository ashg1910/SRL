# SRL
Semantic Role Tagger for LREC 2018

For testing this code, dummy files have been given in the folder '/finalTraining' and '/argument-classification/allTest/finalTest'

To run the code :
Use python version 2.7 or later
Libraries needed - 
sklearn, numpy, gensim, pickle, keras

How to run:
1. -> python prune_sentences.py finalTraining/    #takes out the sentences which don't have pbrole annotation.
2. -> python feature_extraction.py finalTraining/   #when given a propbank data file as input, it creates features of the files in this folder.

In the folder 'wordvecTrain/'

python trainCBOW.py hindi_corpus/   #train a word2Vec model using CBOW

In the folder 'argument-classification/allTest/'    #do the same things

3. -> python prune_sentences.py finalTest/

4. -> python testFeaturesExtraction.py finalTest/

5. -> python testVectorizer.py testFeats.txt    #formed after step 4.
  

In the folder 'argument-classification/' -->

6. -> python clVectorizer.py ../trainFeats.txt     #trainFeats.py is formed after step 2.

7. -> python crossVal.py    #gives out the results after 5 cross validation.



For data set queries, you may contact -> ashg1910@gmail.com
