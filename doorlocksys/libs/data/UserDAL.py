#!/user/bin/env python
from libs.entity.User import User
from libs.api.auth import Auth
import requests
class UserDAL:

	def __init__(self):
		auth = Auth()
		self.URL = auth.URL
		self.headers = {'Content-Type': 'application/json', 'AccessType'
		: 'device' }

	def get_by_id(self,id):
		#query = "Select DeviceActionID, ActionName,IsActive FROM DeviceActions WHERE IsActive = ('%s')" %status
		#db = DbConnect()
		#obj = DevAct()
		#db.cur.execute(query)
		#result = db.cur.fetchone()
		##result is array of [id],[name]
		#if db.cur.rowcount == 1:
		#	obj.id = result[0]
		#	obj.action_name = result[1]
		#	obj.is_active = result[2]
		#return obj
		pass
	
	def get_by_fingerprintid(self,fingerprintid):
		print(1+ fingerprintid)
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"user",'name':"getByFingerprintid",'param':{'fingerprint': fingerprintid}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS)
		# extracting data in json format 
		data = r.json()
		print(data)
		
			
		result = data["response"]["result"]
		obj = User()
		#result is array of [id],[name]
		if result:
			obj.id = result["userID"]
			obj.user_name = result["userName"]
			obj.full_name = result["fullName"]
			obj.fingerprints = result["fingerprints"]
		return obj

	def edit(self,fingerprints):
		# defining a params dict for the parameters to be sent to the API 
		PARAMS = {'src':"user",'name':"editfingerprint",'param':{'fingerprint': fingerprints}}
		# sending get request and saving the response as response object
		r = requests.post(url = self.URL,headers=self.headers, json = PARAMS) 
		# extracting data in json format 
		data = r.json()
		print(data["response"]["status"])
	