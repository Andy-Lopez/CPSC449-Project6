Andy Lopez: adny@csu.fullerton.edu
Brandon Chenze: bchenze@csu.fullerton.edu

Requires Redis
$ sudo apt install --yes redis

Redis-py and 
$ sudo apt install --yes python3-hiredis

To start, please run search.py
python3 search.py

To fill redis with sample data and make sample requests run search.py first, then run sampledata.py
python3 sampledata.py

redis runs on port 6379, search.py runs on 8080

sampledata.py tests using the Requests library. Sample curl commands are in the search.py comments