#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
from gensim.models import Word2Vec,word2vec
from  sys import stdin
import cPickle as pickle
import os
import logging
import sys
import numpy as np
import re

def getChunkTags(var) :
    tags = []
    tags.append(var)

    if var == 'NULL__VGF' :
        tags.append('VGF')

    elif var == 'NULL__NP' :
        tags.append('NP')

    elif var == 'NULL__CCP' :
        tags.append('CCP')

    elif var == 'NULL__VGNF' :
        tags.append('VGNF')

    return tags

def getDrels(var) :
    rels = []
    rels.append(var)

    if var == 'k7p':
        rels.append('k7')

    elif var == 'k2s':
        rels.append('k2')

    elif var == 'k7t':
        rels.append('k7')

    elif var == 'ras-k1':
        rels.append('ras')
        rels.append('k1')

    elif var == 'nmod__relc':
        rels.append('nmod')

    elif var == 'r6-k2':
        rels.append('r6')
        rels.append('k2')

    elif var == 'nmod__k1inv':
        rels.append('nmod')
        rels.append('k1')

    elif var == 'k1s':
        rels.append('k1')

    elif var == 'k4u':
        rels.append('k4')

    elif var == 'r6v':
        rels.append('r6')

    elif var == 'k1u':
        rels.append('k1')

    elif var == 'r6-k1':
        rels.append('r6')
        rels.append('k1')

    elif var == 'pof-idiom':
        rels.append('pof')

    elif var == 'k4a':
        rels.append('k4')

    elif var == 'ras-k2':
        rels.append('ras')
        rels.append('k2')

    elif var == 'nmod__k2inv':
        rels.append('nmod') 
        rels.append('k2')

    elif var == 'nmod__pofinv':
        rels.append('nmod')
        rels.append('pof')

    elif var == 'k2p':
        rels.append('k2')

    elif var == 'k2g':
        rels.append('k2')

    elif var == 'k7pu':
        rels.append('k7')

    elif var == 'vmod__adv':
        rels.append('vmod')
        rels.append('adv')

    elif var == 'sent-adv':
        rels.append('adv')

    elif var == 'k7ts':
        rels.append('k7')

    elif var == 'k2u':
        rels.append('k2')

    elif var == 'ras-r6':
        rels.append('ras')
        rels.append('r6')

    elif var == 'k5prk':
        rels.append('k5')

    elif var == 'ras-k7':
        rels.append('ras')
        rels.append('k7')

    elif var == 'k1g':
        rels.append('k1')

    return rels

    

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


model = word2vec.Word2Vec.load('../wordvecTrain/hindi_aish_w2v.txt')
#model = word2vec.Word2Vec.load_word2vec_format('./wordvecTrain/hindi_w2v.txt')

#model = Word2Vec.load_word2vec_format('./wordvecTrain/hindi_w2v.txt', binary=False, unicode_errors='ignore')

filename = sys.argv[1]

chunkTags = pickle.load(open("../chunkTags.p","rb"))
dRel = pickle.load(open("../dependencyRelations.p","rb"))
arguments = pickle.load(open("../arguments.p","rb"))
frames = pickle.load(open("../frames.p","rb"))
vibhaktis = pickle.load(open("../vibhaktis.p","rb"))
posTags = pickle.load(open("../posTags.p","rb"))
predRawWords = pickle.load(open("../predRawWords.p","rb"))
headRawWords = pickle.load(open("../headRawWords.p","rb"))
morphs = pickle.load(open("../morphs.p","rb"))

#print model["चुना"]
featureVectors = []

counting = 0

with open(filename) as f:
    content = f.readlines()
    for line in content:
        feats = line.split(' ')

        #   predicate as w2v
        # predicate = feats[0]
        # try :
        #    w2v = model[predicate]
        #    vector = w2v
        # except :
        #     vector = np.zeros(30)

        vector = np.zeros(1)
        # #predicate Raw word
        # for w in predRawWords :
        #     if (w.encode('utf-8')) == feats[0] :
        #         vector = np.append(vector, 1)
        #     else :
        #         vector = np.append(vector, 0)

        # #   predicate tag
        # listOfChunkTags = getChunkTags(feats[5])
        # for tag in chunkTags :
        #     found = 0
        #     for x in listOfChunkTags :
        #         if x == tag :
        #             vector = np.append(vector, 1)
        #             found = 1
        #             break
        #     if found == 0 :
        #         vector = np.append(vector, 0)
        # #   predicate Number
        # vector = np.append(vector, int(feats[6]))

        # predicate morph
        predMorph = feats[1]
        for m in morphs :
            if (m.encode('utf-8')) == predMorph :
                vector = np.append(vector, 1)
            else :
                vector = np.append(vector, 0)

        #	chunk tag
        listOfChunkTags = getChunkTags(feats[8])
        for tag in chunkTags :
            found = 0
            for x in listOfChunkTags :
                if x == tag :
                    vector = np.append(vector, 1)
                    found = 1
                    break
            if found == 0 :
                vector = np.append(vector, 0)
            # if tag == feats[8] :
            # 	vector = np.append(vector, 1)
            # else :
            # 	vector = np.append(vector, 0)
        # #	chunk Number
        # vector = np.append(vector, int(feats[9]))

        
        #   FRAME .XX
        word = feats[4].split('.')[0]
        for fi in frames :
            if fi == word :
                vector = np.append(vector, 1)
            else :
                vector = np.append(vector, 0)
        # sense = feats[4].split('.')[1]
        # try :
        #     vector = np.append(vector, int(sense[0]))
        #     vector = np.append(vector, int(sense[1]))
        # except:
        #     vector = np.append(vector, 0)
        #     vector = np.append(vector, 0)

        
        #	parent drel
        listOfDrels = getDrels(feats[10])
        for rel in dRel :
            found = 0
            for x in listOfDrels :
                if x == rel :
                    vector = np.append(vector, 1)
                    found = 1
                    break
            if found == 0 :
                vector = np.append(vector, 0)
            # if rel == feats[10] :
            # 	vector = np.append(vector, 1)
            # else :
            # 	vector = np.append(vector, 0)

        #	parent TAG
        listOfChunkTags = getChunkTags(feats[11])
        for tag in chunkTags :
            found = 0
            for x in listOfChunkTags :
                if x == tag :
                    vector = np.append(vector, 1)
                    found = 1
                    break
            if found == 0 :
                vector = np.append(vector, 0)
        # #parent number
        # vector = np.append(vector, int(feats[12]))

        # # head Raw word
        # for w in headRawWords :
        #     if (w.encode('utf-8')) == feats[7] :
        #         vector = np.append(vector, 1)
        #     else :
        #         vector = np.append(vector, 0)
        #  head word
        head_word = feats[7]
        try :
            w2v = model[head_word]
            vector = np.append(vector, w2v)
        except :
            w2v = np.zeros(30)
            vector = np.append(vector, w2v)


        #   vibhakti
        #   '0' error may be there in vibhaktis.p and featureExtraction.py
        vibhFeats = re.split('_|\+', feats[13].decode('utf-8'))
        for vibh in vibhaktis :
            vibhFlag = 0
            for v in vibhFeats :
                if v == vibh :
                    vibhFlag += 1
            vector = np.append(vector, vibhFlag)
        
        # vibhakti - last words of chunk - W2V
        w2v = np.zeros(30)
        for v in vibhFeats :
            try :
               w2v += model[v]
            except :
                continue
        vector = np.append(vector, w2v)
        
        # vibhakti type
        vORt = 'n'
        rpFlag = 0
        vibhaktiType = feats[14].split('_')
        for vT in vibhaktiType :
            if vT[0] == 'v' :
                vORt = 'v'
            elif vT[0] == 't' :
                vORt = 't'

            if vT == "RP" :
                rpFlag = 1

        if vORt == 'n' :
            #vib or tam
            vector = np.append(vector, -1)
            #RP
            vector = np.append(vector, -1)
            #len
            vector = np.append(vector, -1)
        else :
            if vORt == 'v' :
                vector = np.append(vector, 0)
            elif vORt == 't' :
                vector = np.append(vector, 1)
            #RP
            vector = np.append(vector, rpFlag)
            #len
            vector = np.append(vector, len(vibhaktiType))
        

        # NODE tags
        nodeTags = feats[15].split(',')
        for tag in posTags :
            tagFlag = 0
            for nT in nodeTags :
                if nT == tag :
                    tagFlag += 1
            vector = np.append(vector, tagFlag)
        
        
        # path
        pathUp = feats[16].split(',')[0]
        pathDown = feats[16].split(',')[1]
        pathUp = pathUp.split('+')
        pathDown = pathDown.split('-')
        pLen = len(pathUp) + len(pathDown)
        for obj in pathUp :
            listOfChunkTags = getChunkTags(obj)
            for tag in chunkTags :
                found = 0
                for x in listOfChunkTags :
                    if x == tag :
                        vector = np.append(vector, 1)
                        found = 1
                        break
                if found == 0 :
                    vector = np.append(vector, 0)
        for obj in pathDown :
            listOfChunkTags = getChunkTags(obj)
            for tag in chunkTags :
                found = 0
                for x in listOfChunkTags :
                    if x == tag :
                        vector = np.append(vector, -1)
                        found = 1
                        break
                if found == 0 :
                    vector = np.append(vector, 0)
        pVec = np.zeros(len(chunkTags) * (20 - pLen))
        vector = np.append(vector, pVec)

        #drel-ALL
        drelUp = feats[17].split(',')[0]
        drelDown = feats[17].split(',')[1]
        drelUp = drelUp.split('+')
        drelDown = drelDown.split('-')
        pLen = len(drelUp) + len(drelDown)
        for obj in drelUp :
            listOfDrels = getDrels(obj)
            for rel in dRel :
                found = 0
                for x in listOfDrels :
                    if x == rel :
                        vector = np.append(vector, 1)
                        found = 1
                        break
                if found == 0 :
                    vector = np.append(vector, 0)
        for obj in drelDown :
            listOfDrels = getDrels(obj)
            for rel in dRel :
                found = 0
                for x in listOfDrels :
                    if x == rel :
                        vector = np.append(vector, -1)
                        found = 1
                        break
                if found == 0 :
                    vector = np.append(vector, 0)
        pVec = np.zeros(len(dRel) * (20 - pLen))
        vector = np.append(vector, pVec)

        #path - len
        vector = np.append(vector, pLen)


        #   grand-parent Drel
        listOfDrels = getDrels(feats[18])
        for rel in dRel :
            found = 0
            for x in listOfDrels :
                if x == rel :
                    vector = np.append(vector, 1)
                    found = 1
                    break
            if found == 0 :
                vector = np.append(vector, 0)
        #   grand-parent TAG
        listOfChunkTags = getChunkTags(feats[19])
        for tag in chunkTags :
            found = 0
            for x in listOfChunkTags :
                if x == tag :
                    vector = np.append(vector, 1)
                    found = 1
                    break
            if found == 0 :
                vector = np.append(vector, 0)
        # #grand-parent number
        # vector = np.append(vector, int(feats[20]))


        # voice
        if feats[2] == 'active' :
            vector = np.append(vector, 0)
        elif feats[2] == 'passive' :
            vector = np.append(vector, 1)
        else :
            vector = np.append(vector, -1)

        # speech
        if feats[3] == 'declarative' :
            vector = np.append(vector, 0)
        elif feats[3] == 'imperative' :
            vector = np.append(vector, 1)
        elif feats[3] == 'interrogative' :
            vector = np.append(vector, 2)
        else :
            vector = np.append(vector, -1)

        # UID
        vector = np.append(vector, int(feats[22]))

        # # OUTPUT FOR ARG-IDENTIFY
        # vector = np.append(vector, int(feats[23]))

        # OUTPUT FOR ARG-CLASSIFY
        count = 0
        for arg in arguments :
            count += 1
            if feats[24].rstrip() == arg :
                break
        vector = np.append(vector, count)

        #collect vectors
        featureVectors.append(vector)
        #print len(vector)

X = np.array(featureVectors)
np.save('vectorToTrain.npy', X)
#np.savetxt('vectors.txt', X)