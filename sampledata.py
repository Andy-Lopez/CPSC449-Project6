import requests

#flush redis and enter some sample keywords


url     = 'http://localhost:8080/index'
payload = {"message":"andy", "index":1}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

payload = {"message":"brandon", "index":2}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

payload = {"message":"test", "index":3}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

payload = {"message":"hello", "index":4}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

payload = {"message":"world", "index":5}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

payload = {"message":"foo", "index":6}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

payload = {"message":"Hello World", "index":[2,3]}
headers = {'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)

#Search for given keyword search(keyword)
print("Search for keyword andy")
url     = 'http://localhost:8080/index/keyword/andy'
res = requests.get(url)
print(res.text)

#Search for a keyword not found in the index and returns not found
print("Search for a keyword not found in the index")
url     = 'http://localhost:8080/index/keyword/hi'
res = requests.get(url)
print(res.text)

#Search any(keyword)
print("Search for posts containing any keyword brandon or andy")
url     = 'http://localhost:8080/index/any'
payload = {"keywords":["brandon", "andy", "Hello World"]}
headers = {'Content-Type': 'application/json'}
res = requests.get(url, json=payload, headers=headers)
print(res.text)

#Search for all 
print("Search for posts containing all keywords Hello World or andy")
url     = 'http://localhost:8080/index/all'
payload = {"keywords":["Hello World", "andy"]}
headers = {'Content-Type': 'application/json'}
res = requests.get(url, json=payload, headers=headers)
print(res.text)

#Search with exclusions 
print("Search for any posts containing keywords andy but excluding andy")
url     = 'http://localhost:8080/index/exclude'
payload = {"include":["andy"], "exclude":["andy"]}
headers = {'Content-Type': 'application/json'}
res = requests.get(url, json=payload, headers=headers)
print(res.text)