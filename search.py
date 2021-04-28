import re
import string
import redis
import json
from bottle import route, run, get, post, request, response

stopWords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", 
                "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say",
                "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so",
                "up", "out", "if", "about", "get", "which", "go", "me"]



@post('/index')
def addIndex():
    message = request.json
    messageNew = convert(message['message'])
    messageIndex = message['index']
    for word in messageNew:
        addKeyword(word, messageIndex)
        
    response.body = "Successfully inserted."
    response.status = 201
    return response

#Method to perform preprocessing.
def convert(text):
    text = re.sub("[!\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~]", " ", text)
    text = text.lower()
    myWords = text.split(' ')
    
    
    myWords[:] = [x for x in myWords if x != ""]
    myWords[:] = [x for x in myWords if x not in stopWords]

    return myWords
    

r = redis.StrictRedis(host='localhost',port=6379,db=0)

#Method to insert keyword and index
def insertKeyword(word,index):
    myList = [index]
    try:
        r.set(word, json.dumps(myList))
        #msg = r.get(word)
    except:
        #we will update with the new index
        #updateKeyword()
        print("Error!")
    
#Method to add keyword and index
#If the keyword does not exist create it
def addKeyword(word, index):
    #print(r.get('Hello'))
    try:
        msg = r.get(word)
        newList = json.loads(msg)
        print(newList)
        if index not in newList:
            newList.append(index)
            r.set(word, json.dumps(newList))
        
    except:
        print("Does not exist. Inserting now.")
        insertKeyword(word, index)


    

def deleteAll():
    r = redis.Redis(host="localhost", db=0)
    r.flushdb()



run(host='localhost', port=8080, debug=True)

#insertKeyword()
#updateKeyword("Hello", 27)
#deleteAll()
#x = input()

#print(convert(x))

