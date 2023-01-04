Ashna Jain - Nov 22, 2022
Project 4: Query Scoring 

Breakdown:
    -BM25 (scenes): in query.py lines 30 - 56
    -QL (scenes): in query.py lines 57 - 92
    -BM25 (plays): in query.py lines 93 - 124
    -QL (plays): in query.py lines 125-153
Description:
    Inverted Index:
    ------------------
    -My inverted list data structure is a set of nested dictionaries, with the final value being the number of occurances of a particular word in a scene
        -This was different from P3 where the final value was a array of locations of that word in the specific scene
    
    BM25 Scoring -> Scenes:
    ----------------------
    -I firstly started by getting rid of all duplicate words in the query
    -Then I created a dictionary where each key was a unique word in the query, and the value was the number of occurances in the query

    -I then iterated through all my unique query words and then iterated through the inverted index for each word.
    -For each scene that a word was in, I incremented n and if that scene was the target document, I set f to the number of ocurances of that word in the entire scene.
    -I then calcuated the score, and reset the values of n and f to 0 for the next word

    QL Scoring -> Scenes:
    ---------------------
    -I  set D to the len of the scene by accessing a dictionary I had created during the indexing process, where each key is a scene and the value is the length of the entire scene
    -I iterated through each word's inverted index: for each scene in the index, I incremented cq by the number of occcurances of the word in that scene, and if the scene was equal to the target document, I set fq to the number of occurances. 

    Ranking:
    --------
    -After building the index, I would parse through the queries file, and store the results in an array where each input was a [score, doc]
    -I then sorted the array based off the score and alphabethic order as a tie-breaker. 
    -Finally, I only printed the first 100 entries to the outputFile.

Libraries:
    -import gzip
    -import json
    -import math
    -import os
    -import sys 

Dependencies:
    -Python 3

Building/Running:
    -After directing to the appropiate folder, type "python query.py collection.json.gz queries.tsv outputFile" into terminal
        -After doing this, an outputFile should be created with all the outputs of the queries.