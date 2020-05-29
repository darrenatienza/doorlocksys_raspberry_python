from libs.api.auth import Auth
from libs.entity.DevAct import DevAct
import requests
class DevActDAL:

	def __init__(self):
		auth = Auth()
		#self.URL = "https://darrenapi.000webhostapp.com/doorlocksys-api/"
		self.URL = auth.URL
		self.headers = {'Content-Type': 'application/json', 'AccessType'
		: 'device' }

	def get_all(self):
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"deviceaction",'name':"getall",'param':{}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS) 
		# extracting data in json format 
		data = r.json()
		objs = []
		for item in data["response"]["result"]:
			obj = DevAct()
			obj.id = item["deviceactionID"]
			obj.action_name = item["actionname"]
			obj.is_active = item["isactive"]
			objs.append(obj)

		return objs
	
	def get_by_status(self,status):
		print("Get By Status not implemented")

	def get_active_device_action(self):
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"deviceaction",'name':"getactivedeviceaction",'param':{}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS) 
		# extracting data in json format 
		data = r.json()['response']['result']
		obj = DevAct()
		obj.id = data["deviceactionID"]
		obj.action_name = data["actionname"]
		obj.is_active = data["isactive"]
		return obj

	def disable(self):
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"deviceaction",'name':"setdevicesinactive",'param':{}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS) 
		# extracting data in json format 
		data = r.json()
		print(data["response"]["status"])
		
	
	def editActiveStatus(self,status):
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"deviceaction",'name':"editActiveStatus",'param':{'actionname' : status}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS) 
		# extracting data in json format 
		data = r.json()
		print(data["response"]["status"])

