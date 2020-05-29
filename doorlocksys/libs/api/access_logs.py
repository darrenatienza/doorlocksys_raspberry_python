# importing the requests library 
import requests 
from auth import Auth
# api-endpoint 
URL = "https://darrenapi.000webhostapp.com/doorlocksys-api/"
#URL = "http://localhost:8081/dev/doorlocksys-api/"
# location given here 
token = Auth().generateToken()
headers = {'Content-Type': 'application/json', 'Authorization'
	: ('Bearer {0}').format(token) }
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'src':"accesslog",'name':"getall",'param':{"date": "2020-02-22 00:00:00",
		"criteria": ""}}
  
# sending get request and saving the response as response object
r = requests.post(url = URL,headers=headers, json = PARAMS) 

# extracting data in json format 
data = r.json()
print(data)