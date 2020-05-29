#!/usr/bin/env python
import mysql.connector

class DbConnect:

	def __init__(self):
		self.con = mysql.connector.connect(host="localhost",user="raspi",passwd="raspi",database="DoorLockSys")
		self.cur = self.con.cursor(buffered=True)
		
	def __del__(self):
		#destroy my sql connection
		self.cur.close()
		self.con.close()
