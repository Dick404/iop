#!/usr/bin/python

import sys
import os
import re

class recorder():

    def __init__(self):
        if not os.path.exists("/var/vcap/task"):
            os.system("mkdir -p /var/vcap;touch /var/vcap/task")
        

    def record(self,task):
        writer = open("/var/vcap/task","a+")
        writer.write(task+"\n")
        writer.close()
        return

    def test(self,task):
	print task
        reader = open("/var/vcap/task","r")
        tasks = reader.readlines()
        reader.close()
        for task_solve in tasks:
<<<<<<< HEAD
            if task_solve == (task+"\n"):
=======
            if task_solve == (task+"\n") or task_solve == task:
		print "+++++++++++++++++++++++++++++++++++++++++++++++"
>>>>>>> ef9a2dc2c96edb177139717b326ae6e4c6d13781
                return False
        return True

