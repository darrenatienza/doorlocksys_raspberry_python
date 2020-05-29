#!/user/bin/env python
from libs.data.DoorAccessLogDAL import DoorAccessLogDAL

class DoorAccessLogBLL:
    
    def __init__(self):
        self.data = DoorAccessLogDAL()
    
    def add(self,userid,logs):
        self.data.add(userid,logs)