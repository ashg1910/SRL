#!/usr/bin/python 

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
            
    for fileName in newFileList :
        d = ssfAPI.Document(fileName)
        writeTo = './finalTest/' + fileName.split('/')[-1]
        f = open(writeTo,'w')
        #print f
        sentIndex = 0
        for tree in d.nodeList :
            try :
            	flag_pbrel = 0
                tree.populateNodes(naming='strict')
                tree.populateEdges()
                for chunkNode in tree.nodeList :
                    if chunkNode.parentPB != '0' :
                    	flag_pbrel=1
                    	break
                if flag_pbrel == 1:
                	string = ""
                	sentIndex += 1
            		string += "<Sentence id='" + str(sentIndex) + "'>"
            		string += tree.text
            		#print string
            		string += "</Sentence>\n"
            		u = string.encode("utf-8")
            		f.write(u)
            
            except : 
                continue

        f.close()