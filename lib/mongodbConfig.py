#!/usr/bin/python

import sys
import os
import re

def install():
    os.system("yum -y install mongodb-server mongodb")
    return

def getLocalIp():
    ip_list = []
    reader = os.popen("ip addr")
    temps = reader.readlines()
    for temp in temps:
	result = re.search(r"inet (\d+\.\d+\.\d+\.\d+)/\d+ (scope|brd)",temp)
	if result:
	   print result.group(0)
	   ip_list.append(result.group(1))
    return ip_list
    

def config(ips):
    ip = ips[0]
    for i in range(1,len(ips)):
	ip += ","+ips[i]
    reader = open("./config/mongod.conf","r")
    writer = open("/etc/mongod.conf","w")
    text = reader.readlines()
    reader.close()
    writer.writelines(text)
    writer.write("bind_ip = "+ip)
    return

def run():
    os.system("systemctl enable mongod.service")
    os.system("systemctl start mongod.service")
    return

def create(ip='127.0.0.1',user="ceilometer",pwd="123456a?",roles="dbAdmin"):
    os.system("mongo --host "+ip+" --eval 'db = db.getSiblingDB(\"ceilometer\");db.createUser({user: \""+user+"\",pwd: \""+pwd+"\",roles: [ \"readWrite\", \""+roles+"\" ]})'")
    return
