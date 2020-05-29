#!/user/bin/env python
from libs.entity.DoorAccessLog import DoorAccessLog
from libs.api.auth import Auth
import requests
class DoorAccessLogDAL:

	def __init__(self):
		auth = Auth()
		self.URL = auth.URL
		self.headers = {'Content-Type': 'application/json', 'AccessType'
		: 'device' }

	def add(self,userid,logs):
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"accesslog",'name':"add",'param':{'userid' : userid, 'logs': logs}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS) 
		# extracting data in json format 
		data = r.json()
		print(data["response"]["status"])