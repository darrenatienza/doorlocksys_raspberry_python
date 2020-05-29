# importing the requests library 
import requests 

class Auth:

    def __init__(self):
        # api-endpoint
        self.URL = "https://dooraccess.000webhostapp.com/api/"
        #self.URL = "http://192.168.1.129:8081/api/doorlocksys-api/"
    
    def generateToken(self):
        # location given here 
        username = "admin"
        password = "admin"
        headers = {'Content-Type': 'application/json'}
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {'src':"token",'name':"generatetoken",'param':{'username': username, 'password':password}} 

        # sending get request and saving the response as response object
        r = requests.post(url = self.URL,headers=headers, json = PARAMS) 

        # extracting data in json format 
        data = r.json()
        return data["response"]["result"]["token"]
            


