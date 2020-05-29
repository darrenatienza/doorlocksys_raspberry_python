#!/user/bin/env python
from libs.data.DevActDAL import DevActDAL
class DevActBLL:
    
    def __init__(self):
        self.data = DevActDAL()
    
    def get_all(self,criteria):
        return self.data.get_all(criteria)

    def get_by_status(self,status):
        return self.data.get_by_status(status) 

    def get_active_device_action(self):
        return self.data.get_active_device_action() 
    
    def setDeviceAction(self, action):
        self.data.disable()
        self.data.editActiveStatus(action)
