#!/usr/bin/python 

import ssfAPI
import sys
import cPickle as pickle

def folderWalk(folderPath):
    import os
    fileList = []
    for dirPath , dirNames , fileNames in os.walk(folderPath) :
        for fileName in fileNames : 
            fileList.append(os.path.join(dirPath , fileName))
    return fileList

if __name__ == '__main__' :
    
    inputPath = sys.argv[1]
    fileList = folderWalk(inputPath)
    newFileList = []
    for fileName in fileList :
        xFileName = fileName.split('/')[-1]
        if xFileName == 'err.txt' or xFileName.split('.')[-1] in ['comments','bak'] or xFileName[:4] == 'task' :
            continue
        else :
            newFileList.append(fileName)
    

    uid = 0
    maxPath = 0
    chunkTags = []
    drelations = []
    f = open('testFeats.txt','w')
    for fileName in newFileList :
        d = ssfAPI.Document(fileName)
        print fileName
        # writeTo = './FinalTraining/' + fileName.split('/')[-1]
        # f = open(writeTo,'w')
        #print f
        for tree in d.nodeList :
            try :
                tree.populateNodes(naming='strict')
                tree.populateEdges()
                #countChunk = 0
                heightDict = {}
                parDict = {}
                predicates = []
                for chunkNode in tree.nodeList :
                    for node in chunkNode.nodeList :
                        if node.getAttribute('pbrole') != None :
                            breakFlag = 1
                            predicates.append(chunkNode)
                    h = 0
                    tempChunk = chunkNode
                    while tempChunk!='0' :
                        h += 1
                        if tempChunk.parent == '0' :
                            tempChunk = '0'
                        else :
                            parName = tempChunk.parent
                            if parName.split('_')[0] == 'NULL' :
                                for chunk in tree.nodeList :
                                    if chunk.name == parName or chunk.type == parName :
                                        parDict[tempChunk] = chunk
                                        tempChunk = chunk
                                        break
                            else :
                                for chunk in tree.nodeList :
                                    if chunk.name == parName :
                                        parDict[tempChunk] = chunk
                                        tempChunk = chunk
                                        break

                    if tempChunk=='0' :
                        heightDict[chunkNode] = h

                for chunkNode in tree.nodeList :
                    for verbPredicate in predicates :
                        c1 = chunkNode
                        c2 = verbPredicate
                        pathUp = ""
                        pathDown = ""
                        drelUp = ""
                        drelDown = ""
                        pLen = 0
                        while heightDict[c1] and heightDict[c2] :
                            if heightDict[c1] > heightDict[c2] :
                                pathUp += c1.type + '+'
                                if c1.parentRelation != 'root' :
                                    drelUp += c1.parentRelation + '+'
                                else :
                                    drelUp += 'None' + '+'
                                c1 = parDict[c1]
                                pLen += 1
                            elif heightDict[c1] < heightDict[c2] :
                                pathDown +=  '-' + c2.type
                                if c2.parentRelation != 'root' :
                                    drelDown += '-' + c2.parentRelation
                                else :
                                    drelDown += '-' + 'None'
                                c2 = parDict[c2]
                                pLen += 1
                            else :
                                if c1 == c2 :
                                    pathUp += c1.type
                                    pLen += 1
                                    break
                                else :
                                    pathUp += c1.type + '+'
                                    if c1.parentRelation != 'root' :
                                        drelUp += c1.parentRelation + '+'
                                    else :
                                        drelUp += 'None' + '+'
                                    pathDown +=  '-' + c2.type
                                    if c2.parentRelation != 'root' :
                                        drelDown += '-' + c2.parentRelation
                                    else :
                                        drelDown += '-' + 'None'
                                    c1 = parDict[c1]
                                    c2 = parDict[c2]
                                    pLen += 2

                        path = pathUp + ',' + pathDown
                        drelPath = drelUp + ',' + drelDown
                        maxPath = max(maxPath, pLen)
                # for chunkNode in tree.nodeList :
                #     #countChunk += 1
                #     #print countChunk
                #     #print 'main', chunkNode.name
                #     tempChunk = chunkNode
                #     if tempChunk.parent == '0' :
                #             tempChunk = '0'
                #     else :
                #         parName = tempChunk.parent
                #         if parName.split('_')[0] == 'NULL' :
                #             for chunk in tree.nodeList :
                #                 if chunk.name == parName or chunk.type == parName :
                #                     tempChunk = chunk
                #                     break
                #         else :
                #             for chunk in tree.nodeList :
                #                 if chunk.name == parName:
                #                     tempChunk = chunk
                #                     break
                                    
                #     predicate = '0'
                #     predicateChunkTag = ""
                #     predicateChunkNum = ""
                #     breakFlag = -1
                #     while tempChunk != '0' and breakFlag==-1 :
                #         verbChunkTags = ["VGF", "VGNF", "VGNN", "NULL__VGF", "NULL__VGNF"]
                #         if tempChunk.type in verbChunkTags :
                #             breakFlag = 0
                #             for node in tempChunk.nodeList :
                #                 if node.getAttribute('pbrole') != None :
                #                     breakFlag = 1
                #                     predicate = node.lex
                #                     predicateRel = node.getAttribute('pbrole')
                #                     break

                #         if breakFlag == 1 :
                #             if tempChunk.getAttribute('voicetype') :
                #                 voicetype = tempChunk.getAttribute('voicetype')
                #             else :
                #                 voicetype = 'None'

                #             if tempChunk.getAttribute('stype') :
                #                 stype = tempChunk.getAttribute('stype')
                #             else :
                #                 stype = 'None'

                #             predicateChunkTag = tempChunk.type

                #             if tempChunk.name[-1] >= '0' and tempChunk.name[-1] <='9' :
                #                 if tempChunk.name[-2] >= '0' and tempChunk.name[-2] <='9' :
                #                     predicateChunkNum = str(tempChunk.name[-2]) + str(tempChunk.name[-1])
                #                 else :
                #                     predicateChunkNum = str(tempChunk.name[-1])
                #             else :
                #                 predicateChunkNum = '1'

                #             break

                #         if tempChunk.parent == '0' :
                #             tempChunk = '0'
                #         else :
                #             parName = tempChunk.parent
                #             if parName.split('_')[0] == 'NULL' :
                #                 for chunk in tree.nodeList :
                #                     if chunk.name == parName or chunk.type == parName :
                #                         tempChunk = chunk
                #                         break
                #             else :
                #                 for chunk in tree.nodeList :
                #                     if chunk.name == parName:
                #                         tempChunk = chunk
                #                         break

                #     ##leaving chunks not having any predicate
                #     if predicate != '0' :
                        feats = ""
                        
                        # predicate
                        for node in verbPredicate.nodeList :
                            if node.getAttribute('pbrole') != None :
                                breakFlag = 1
                                pred = node.lex
                                predRel = node.getAttribute('pbrole')
                                predMorph = (node.fsList[0].split(' ')[1]).split(',')[-2]
                                break
                        
                        feats += pred + ' '

                        #pred Morph
                        feats += predMorph + ' '

                        # voice
                        if verbPredicate.getAttribute('voicetype') :
                            voicetype = verbPredicate.getAttribute('voicetype')
                        else :
                            voicetype = 'None'
                        feats += voicetype + ' '

                        # speech
                        if verbPredicate.getAttribute('stype') :
                            stype = verbPredicate.getAttribute('stype')
                        else :
                            stype = 'None'
                        feats += stype + ' '
                        
                        # FRAME
                        feats += str(predRel) + ' '

                        # Predicate chunk tag and number
                        predicateChunkTag = verbPredicate.type

                        if verbPredicate.name[-1] >= '0' and verbPredicate.name[-1] <='9' :
                            if verbPredicate.name[-2] >= '0' and verbPredicate.name[-2] <='9' :
                                predicateChunkNum = str(verbPredicate.name[-2]) + str(verbPredicate.name[-1])
                            else :
                                predicateChunkNum = str(verbPredicate.name[-1])
                        else :
                            predicateChunkNum = '1'
                        
                        feats += predicateChunkTag + ' '
                        feats += predicateChunkNum + ' '

                        # head word
                        feats += chunkNode.getAttribute('head') + ' '
                        
                        # chunk TAG
                        feats += str(chunkNode.type) + ' '
                        
                        # chunk naming number
                        if chunkNode.name[-1] >= '0' and chunkNode.name[-1] <='9' :
                            if chunkNode.name[-2] >= '0' and chunkNode.name[-2] <='9' :
                                feats += str(chunkNode.name[-2]) + str(chunkNode.name[-1]) + ' '
                            else :
                                feats += str(chunkNode.name[-1]) + ' '
                        else :
                            feats += '1' + ' '
                        
                        ## drel addition
                        parent = '0'
                        parentRelation = '0'
                        if chunkNode.getAttribute('drel') != None :
                            drelList = chunkNode.getAttribute('drel').split(':')
                            if len(drelList) == 2 :
                                parent = drelList[1]
                                parentRelation = chunkNode.getAttribute('drel').split(':')[0]

                        elif chunkNode.getAttribute('dmrel') != None :
                            drelList = chunkNode.getAttribute('dmrel').split(':')
                            if len(drelList) == 2 :
                                parent = drelList[1]
                                parentRelation = chunkNode.getAttribute('dmrel').split(':')[0]
                        
                        # Relation TAG
                        if parentRelation != '0' :
                            
                            feats += str(parentRelation) + ' '
                        else :
                            feats += 'None' + ' '

                        # parent NAME and NUMBER
                        if parent != '0' :
                            num = ""
                            if parent[-1] >='0' and parent[-1] <='9' :
                                if parent[-2] >='0' and parent[-2] <='9' :
                                    num += parent[-2] + parent[-1]
                                    parent = parent[:len(parent)-2]
                                else :
                                    num += parent[-1]
                                    parent = parent[:len(parent)-1]
                            else :
                                num += '1'
                            feats += str(parent) + ' '
                            feats += num + ' '
                        else :
                            feats += 'None' + ' '
                            feats += '0' + ' '
                            

                        # chunk's VIBHAKTI
                        try :
                            vibh = (chunkNode.fsList[0].split(' ')[1]).split(',')[-2]
                        except :
                            vibh = '0'

                        if vibh == '' :
                            vibh = '0'
                        
                        feats += vibh + ' '

                        # Chunk VIBHAKTI type:
                        vibType = 'None'
                        if chunkNode.getAttribute('vpos') != None :
                            vibType = chunkNode.getAttribute('vpos')    
                        feats += vibType + ' '

                        
                        # pos tags of nodes in chunk
                        headPOS = 'None'
                        if len(chunkNode.nodeList) > 0 :
                            for node in chunkNode.nodeList :
                                if node.name == chunkNode.getAttribute('head') :
                                    headPOS = str(node.type)
                                    break
                        feats += str(headPOS) + ' '

                        # # Argument Parent tag
                        # argTag = chunkNode.parentPB
                        # tagNum = '0'
                        # if argTag != '0' :
                        #     if argTag[-1] >= '0' and argTag[-1] <='9' :
                        #         if argTag[-2] >= '0' and argTag[-2] <='9' :
                        #             tagNum = str(argTag[-2]) + str(argTag[-1])
                        #             argTag = argTag[:-2]
                        #         else :
                        #             tagNum = str(argTag[-1])
                        #             argTag = argTag[:-1]
                        #     else :
                        #         tagNum = '1'
                        # feats += argTag + ' ' + tagNum + ' '

                        # path
                        feats += path + ' '

                        # drel Path
                        feats += drelPath + ' '

                        #grand-Parent
                        try :
                            tempChunk = parDict[chunkNode]
                            if tempChunk.parentRelation != 'root' :
                                feats += str(tempChunk.parentRelation) + ' '
                            else :
                                feats += 'None' + ' '
                            # parent TAG and NUMBER
                            if tempChunk.parent != '0' :
                                num = ""
                                if tempChunk.parent[-1] >='0' and tempChunk.parent[-1] <='9' :
                                    if tempChunk.parent[-2] >='0' and tempChunk.parent[-2] <='9' :
                                        num += tempChunk.parent[-2] + tempChunk.parent[-1]
                                        tempChunk.parent = tempChunk.parent[:len(tempChunk.parent)-2]
                                    else :
                                        num += tempChunk.parent[-1]
                                        tempChunk.parent = tempChunk.parent[:len(tempChunk.parent)-1]
                                else :
                                    num += '1'
                                feats += str(tempChunk.parent) + ' '
                                feats += num + ' '
                            else :
                                feats += 'None' + ' '
                                feats += '0' + ' '
                        except :
                            feats += 'None' + ' '
                            feats += 'None' + ' '
                            feats += '0' + ' '


                        # filename and sentence index
                        feats += str(fileName)+','+str(tree.name)+ ' '

                        # UID
                        uid += 1
                        feats += str(uid) + ' '

                        ## check if arg or not
                        argument = '0'
                        if chunkNode.getAttribute('pbrel') != None :
                            argument = '1'
                        elif chunkNode.getAttribute('pbmrel') != None :
                            argument = '1'

                        feats += str(argument) + ' '

                        ## argument TYPE
                        argType = chunkNode.parentArgument
                        feats += str(argType)


                        feats += '\n'
                        #print feats
                        f.write(feats.encode('utf8'))

            except : 
                continue

    print maxPath

    f.close()