from libs.data.UserDAL import UserDAL

item = UserDAL().get_by_fingerprintid(1)
print(item.user_name)

