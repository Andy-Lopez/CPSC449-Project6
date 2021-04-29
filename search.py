import re
import string
import redis
import json
from bottle import route, run, get, post, request, response

stopWords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", 
                "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say",
                "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so",
                "up", "out", "if", "about", "get", "which", "go", "me"]

r = redis.StrictRedis(host='localhost',port=6379,db=0)

#Endpoint to add text to the index
#curl -d '{"message":"brandon", "index":6}' -H 'Content-Type: application/json' http://localhost:8080/index

@post('/index')
def addIndex():
    message = request.json
    messageNew = convert(message['message'])
    messageIndex = message['index']
    for word in messageNew:
        #add keyword checks to see if it already exist
        addKeyword(word, messageIndex)

    response.body = "Successfully inserted."
    response.status = 201
    return response


#Endpoint to get postids that contain any of the keywords
#curl -d '{"keywords":["hello", "brandon"]}' -H 'Content-Type: application/json' -X GET http://localhost:8080/index/any

@get('/index/any')
def getAny():
    myIndex = []
    message = request.json
    for mes in message['keywords']:
        try:
            index = json.loads(r.get(mes))
            print(index)
            for i in index:
                if i not in myIndex:
                    myIndex.append(i)
        except:
            print(mes + " is not in the db.")
            #response.status = 400
            #response.body = "Something went wrong..."
            #RETURN ERROR

    return json.dumps(myIndex)

#Endpoint to get postids that contain any of the keywords
#curl -d '{"keywords":["hello", "brandon"]}' -H 'Content-Type: application/json' -X GET http://localhost:8080/index/any

@get('/index/search/<keyword>')
def getSpecific(keyword):
    myIndex = []
    try:
        index = json.loads(r.get(keyword))
        print(index)
        for i in index:
            if i not in myIndex:
                myIndex.append(i)
    except: 
        response.status = 400
        response.body = "Could not find keyword"
        return response

    return json.dumps(myIndex)

#Endpoint to get postid that contains all the keywords
# curl -d '{"keywords":["hello", "world"]}' -H 'Content-Type: application/json' -X GET http://localhost:8080/index/all 

@get('/index/all')
def getAll():
    message = request.json
    myIndex = []
    empty = True
    for mes in message['keywords']:
        try:
            index = json.loads(r.get(mes))
            if(empty):
                myIndex = index
                empty = False
            else:
                myIndex = list(set(myIndex) & set(index))
        except: 
            print("Nope!")
            #response.status = 400
            #response.body = "Something went wrong..."
            #RETURN ERROR
        
    response.body = json.dumps(myIndex)
    response.status = 200
    return response


#curl -d '{"include":["hello", "brandon"], "exclude":[]}' -H 'Content-Type: application/json' -X GET http://localhost:8080/index/exclude
@get('/index/exclude')
def getExclude():
    message = request.json
    include = []
    exclude = []

    for mes in message['include']:
        try:
            index = json.loads(r.get(mes))
            for i in index:
                if i not in include:
                    include.append(i)
        except:
            print("Error")
            #RETURN ERROR

    for mes in message['exclude']:
        try:
            index = json.loads(r.get(mes))
            for i in index:
                if i not in exclude:
                    exclude.append(i)
        except:
            print("Error") 
            #RETURN ERROR

    response.body = json.dumps(list(set(include) - set(exclude)))
    return response


#Method to perform preprocessing.
def convert(text):
    text = re.sub("[!\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~]", " ", text)
    text = text.lower()
    myWords = text.split(' ')
    
    
    myWords[:] = [x for x in myWords if x != ""]
    myWords[:] = [x for x in myWords if x not in stopWords]

    return myWords
    



#Method to insert keyword and index
def insertKeyword(word,index):
    myList = [index]
    try:
        r.set(word, json.dumps(myList))
    except:
        print("Error!")
    return 
    
#Method to add keyword and index
#If the keyword does not exist create it
def addKeyword(word, index):
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

    return 

    

def deleteAll():
    r = redis.Redis(host="localhost", db=0)
    r.flushdb()

    return



run(host='localhost', port=8080, debug=True)

#insertKeyword()
#updateKeyword("Hello", 27)
#deleteAll()
#x = input()

#print(convert(x))

