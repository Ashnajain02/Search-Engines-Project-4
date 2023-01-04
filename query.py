#Ashna Jain
#Project 4: Query Scoring

import gzip
import json
import math
import os
import sys 

inverted_index = dict()
k1 = 1.8
k2 = 5
b = 0.75
u = 300

scenes = set()
dlScenes = dict()
avdlScenes = 0

plays = set()
dlPlays = dict()
avdlPlays = 0
C = 0

def BM25Scene(query, document):
    score = 0

    qf = dict()
    query_words = (" ".join(sorted(set(query), key=query.index))).split()
    for word in query_words:
        qf[word] = query.count(word)
  
    f = 0
    n = 0
    for word in query_words:
        if word in inverted_index.keys():
            for play in inverted_index[word]:
                for scene in inverted_index[word][play]:
                    n += 1
                    if scene == document:
                        f = inverted_index[word][play][scene]

        K = k1*((1-b)+b*dlScenes[document]/avdlScenes)
        num = math.log((NScene-n+0.5)/(n+0.5))* ((k1+1)*f)/(K+f) * ((k2+1)*qf[word])/(k2+qf[word])
        score += num

        n = 0
        f = 0
        
    return score

def QLScene(query, document):
    score = 0
    query_words = query
    
    fq = 0
    cq = 0
    D = dlScenes[document]
    containsQueryTerms = False

    for word in query_words:
        if word in inverted_index.keys():
            for play in inverted_index[word]:
                for scene in inverted_index[word][play]:
                    cq += inverted_index[word][play][scene]
                    if scene == document:
                        containsQueryTerms = True
                        fq = inverted_index[word][play][scene]

        num = math.log( ( fq + (u*cq/C) ) / (D + u) )
        score += num

        cq = 0
        fq = 0
    
    if containsQueryTerms == False:
        return 0
    
    return score

def BM25Play(query, document):
    score = 0

    qf = dict()
    query_words = (" ".join(sorted(set(query), key=query.index))).split()
    for word in query_words:
        qf[word] = query.count(word)
  
    f = 0
    n = 0
    for word in query_words:
        if word in inverted_index.keys():
            for play in inverted_index[word]:
                n += 1
                if play == document:
                    for scene in inverted_index[word][play]:
                        f += inverted_index[word][play][scene]
                    

        K = k1*((1-b)+b*dlPlays[document]/avdlPlays)
        num = math.log((NPlays-n+0.5)/(n+0.5)) * ((k1+1)*f)/(K+f) * ((k2+1)*qf[word])/(k2+qf[word])
        score += num

        n = 0
        f = 0
        
    return score

def QLPlay(query, document):

    score = 0
    query_words = query
    
    fq = 0
    cq = 0
    D = dlPlays[document]
    containsQueryTerms = False

    for word in query_words:
        if word in inverted_index.keys():
            for play in inverted_index[word]:
                for scene in inverted_index[word][play]:
                    cq += inverted_index[word][play][scene]
                    if play == document:
                        fq += inverted_index[word][play][scene]
                        containsQueryTerms = True

        num = math.log( (fq+(u*cq/C)) / (D + u) )
        score += num

        cq = 0
        fq = 0

    if containsQueryTerms == False:
        return 0
    return score

 
#query collection.json.gz queries.tsv outputFile
if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'shakespeare-scenes.json.gz'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'playQueries.tsv'
    outputFile = sys.argv[3] if argv_len >= 4 else 'playQueries.results'
    

    with gzip.open(inputFile, "rt") as file:
        data = json.load(file)

        NScene = len(data['corpus'])

        for elem in data['corpus']:
            playID = elem['playId']
            sceneID = elem['sceneId']
            sceneNum = elem['sceneNum']
            text = elem['text'].split()

            
            scenes.add(sceneID)
            dlScenes[sceneID] = len(text)


            plays.add(playID)
            if playID not in dlPlays:
                dlPlays[playID] = 0
        
            dlPlays[playID] += len(text)

            C += len(text)

            for word in text: 
                if inverted_index.get(word) == None: 
                    inverted_index[word] = dict()
                    inverted_index[word][playID] = dict() 
                    inverted_index[word][playID][sceneID] = 1
                elif word in inverted_index and playID not in inverted_index[word].keys():
                    inverted_index[word][playID] = dict() 
                    inverted_index[word][playID][sceneID] = 1
                elif word in inverted_index and sceneID not in inverted_index[word][playID].keys():
                    inverted_index[word][playID][sceneID] = 1
                else:
                    inverted_index[word][playID][sceneID] += 1

        avdlScenes = C / NScene
        NPlays = len(dlPlays)
        avdlPlays = C / NPlays

       
        with open(queriesFile, "r") as file:
            for query in file:
                elem = query.rstrip().split('\t')
                queryName = elem[0]
                scenePlay = elem[1]
                queryType = elem[2]
                inputQuery = elem[3:]
                result = []

                if scenePlay.lower() == 'scene':
                    if queryType.lower() == 'bm25':
                        for doc in scenes:
                            if BM25Scene(inputQuery, doc) != 0:
                                result += [[BM25Scene(inputQuery, doc), doc]]

                    elif queryType.lower() == 'ql':
                        for doc in scenes:
                            if(QLScene(inputQuery, doc) != 0):
                                result += [[QLScene(inputQuery, doc), doc]]

                elif scenePlay.lower() == 'play':
                    if queryType.lower() == 'bm25':
                        for doc in plays:
                            if BM25Play(inputQuery, doc) != 0:
                                result += [[BM25Play(inputQuery, doc), doc]]

                    elif queryType.lower() == 'ql':
                        for doc in plays:
                            if(QLPlay(inputQuery, doc) != 0):
                                result += [[QLPlay(inputQuery, doc), doc]]

                
                with open(outputFile, 'a') as file:
                    result.sort(key=lambda x: -x[0])
                    rank = 1
                    for x in result:
                        if(rank == 101):
                            break
                        file.write(queryName)
                        file.write(' ')
                        file.write("skip")
                        file.write(' ')
                        file.write(x[1])
                        file.write(' ')
                        file.write(str(rank))
                        file.write(' ')
                        file.write(str(x[0]))
                        file.write(' ')
                        file.write("ashnajain")
                        file.write('\n')
                        rank += 1
                