#!/user/bin/env python
from libs.data.UserDAL import UserDAL

class UserBLL:
    
    def __init__(self):
        self.data = UserDAL()
    

    def edit(self,fingerprints):
        return self.data.edit(fingerprints)
    
    def get_by_fingerprintid(self,fingerprintid):
        return self.data.get_by_fingerprintid(fingerprintid)