import ssfAPI 
import sys

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
    
    sentIndex = 0
    f = open('w2v_sentences.txt','w')
    for fileName in newFileList :
        d = ssfAPI.Document(fileName)
        #print fileName
        # writeTo = './FinalTraining/' + fileName.split('/')[-1]
        # f = open(writeTo,'w')
        #print f
        for tree in d.nodeList :
            sentence = ""
            try :
                tree.populateNodes(naming='strict')
                tree.populateEdges()
                sentIndex += 1
                #print sentIndex
                #countChunk = 0
                for chunkNode in tree.nodeList :
                    for node in chunkNode.nodeList :
                        if node.lex != "NULL" :
                            sentence += node.lex + ' '
                sentence += '\n'
                f.write(sentence.encode('utf8'))
            except : 
                continue
    f.close()