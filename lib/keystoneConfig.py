#!/usr/bin/python
import sys
import re
import os


def set_keystone(ip,token):
    configs_new = []
    reader = open("./config/keystone.conf","r")
    writer = open("/etc/keystone/keystone.conf","w")
    configs = reader.readlines()
    reader.close()
    for config in configs:
        if re.match(r"admin_token = (\w+)",config):
	    configs_new.append(re.sub("= (\w+)","= "+token,config))
	elif re.match(r"connection = .*",config):
            configs_new.append(re.sub("= .*$","= mysql://keystone:123456a?@"+ip+":33060/keystone",config))
	else :
	    configs_new.append(config)
    writer.writelines(configs_new)
    writer.close()
    order = 'su -s /bin/sh -c \"keystone-manage db_sync\" keystone'
    print order 
    os.system(order)
    return
